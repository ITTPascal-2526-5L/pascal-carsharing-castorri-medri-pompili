from flask import Blueprint, render_template, redirect, session, request
import json
import os
from werkzeug.utils import secure_filename

user_bp = Blueprint("user", __name__)

DATABASE_PATH = "DataBase/utenti.json"
LICENSES_FOLDER = "app/routes/licenses"

def load_users():
    try:
        with open(DATABASE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(DATABASE_PATH, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def get_current_user():
    if 'username' not in session:
        return None
    username = session.get('username')
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

@user_bp.route("/user_dashboard")
def user_dashboard():
    if 'username' not in session:
        return redirect("/login")
    
    user = get_current_user()
    if not user:
        return redirect("/login")
    
    is_driver = session.get('is_driver', False)  
    return render_template("base_page/base_user.html", utente=user, is_driver=is_driver) 

@user_bp.route("/profile")
def profile():
    if 'username' not in session:
        return redirect("/login")
    
    user = get_current_user()
    if not user:
        return redirect("/login")
    
    return render_template("user/profile.html", utente=user)

@user_bp.route("/settings")
def settings():
    if 'username' not in session:
        return redirect("/login")
    
    user = get_current_user()
    if not user:
        return redirect("/login")
    
    return render_template("user/settings.html", utente=user)

@user_bp.route("/become_driver_page")
def become_driver_page():
    if 'username' not in session:
        # Se l'utente non è loggato, portalo alla registrazione e segnala
        # l'intenzione di diventare driver tramite query string
        return redirect("/registration?become_driver=1")
    
    user = get_current_user()
    if not user:
        return redirect("/login")
    
    # Se è già driver, reindirizza al dashboard
    if user.get('driver', False):
        return redirect("/user_dashboard")
    
    # Passa i dati esistenti per precompilare il form
    is_driver = session.get('is_driver', False)
    return render_template("signin/signin_driver.html", utente=user, is_driver=is_driver)

@user_bp.route("/save_driver_upgrade", methods=["POST"])
def save_driver_upgrade():
    if 'username' not in session:
        return redirect("/login")
    
    username = session.get('username')
    users = load_users()
    
    user_found = False
    for user in users:
        if user['username'] == username:
            user_found = True
            # Leggi valori dal form
            nrTel = request.form.get('nrTel', '').strip()
            nrLicense = request.form.get('nrLicense', '').strip()
            name = request.form.get('name', '').strip()
            surname = request.form.get('surname', '').strip()

            # Validazioni lato server
            if len(nrTel) != 10 or not nrTel.isdigit():
                return render_template("signin/signin_driver.html", errore="Numero di telefono non valido (10 cifre)", utente=user)
            if len(nrLicense) < 3:
                return render_template("signin/signin_driver.html", errore="Numero di patente non valido", utente=user)
            if not name or not surname:
                return render_template("signin/signin_driver.html", errore="Nome e cognome richiesti", utente=user)

            # Aggiorna i dati del driver e anagrafici
            user['name'] = name
            user['surname'] = surname
            user['nrTel'] = nrTel
            user['nrLicense'] = nrLicense
            user['driver'] = True
            
            # Gestisci il file della licenza
            if 'license' in request.files:
                file = request.files['license']
                if file and file.filename != '':
                    os.makedirs(LICENSES_FOLDER, exist_ok=True)
                    filename = secure_filename(f"{username}_{nrLicense}")
                    filepath = os.path.join(LICENSES_FOLDER, filename)
                    file.save(filepath)
                    user['license'] = filepath
            
            break
    
    if user_found:
        save_users(users)
        session['is_driver'] = True
        return redirect("/user_dashboard")
    
    return redirect("/login")

@user_bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return redirect("/")

@user_bp.route("/update_settings", methods=["POST"])
def update_settings():
    if 'username' not in session:
        return redirect("/login")
    
    username = session.get('username')
    users = load_users()
    
    for user in users:
        if user['username'] == username:
            user['name'] = request.form.get('name', user.get('name', ''))
            user['surname'] = request.form.get('surname', user.get('surname', ''))
            user['email'] = request.form.get('email', user.get('email', ''))
            user['nrTel'] = request.form.get('nrTel', user.get('nrTel', ''))
            break
    
    save_users(users)
    return redirect("/profile")

@user_bp.route("/delete_account", methods=["POST"])
def delete_account():
    if 'username' not in session:
        return redirect("/login")
    
    username = session.get('username')
    users = load_users()
    
    # Filtra l'utente da eliminare
    users = [u for u in users if u['username'] != username]
    
    save_users(users)
    session.clear()
    return redirect("/")

# Mantieni le vecchie rotte per compatibilità
@user_bp.route("/user_driver")
def user_driver():
    if 'username' in session.keys():
        return redirect("/user_dashboard")
    else:
        return "No session data found"

@user_bp.route("/user_passenger")
def user_passenger():
    if 'username' in session.keys():
        return redirect("/user_dashboard")
    else:
        return redirect("/login") 