from flask import Blueprint, render_template, redirect, request, session, flash
import json
import os

registration_bp = Blueprint("registration", __name__)

# Registrazione unificata - tutti gli utenti come passengers di default
@registration_bp.route("/registration")
def registration():
    # Se viene passato il flag become_driver=1, lo inoltriamo al template
    become_driver = request.args.get('become_driver')
    return render_template("signin/signin_user.html", become_driver=become_driver)

# Per compatibilità con link vecchi
@registration_bp.route("/registration_passenger")
def registration_passenger():
    return render_template("signin/signin_user.html")

@registration_bp.route("/save_user", methods=["POST"])
def save_user():
    username = request.form['username']
    password = request.form['password']
    password_confirm = request.form.get('password_confirm', '')
    email = request.form['email']
    name = request.form.get('name', '').strip()
    surname = request.form.get('surname', '').strip()

    # da aggiungere la crazione della cartella e dei file...guarda nel branch luca
    
    # Validazioni
    if "@" not in email:
        return render_template("signin/signin_user.html", errore="Email non valida")
    if len(password) < 8:
        return render_template("signin/signin_user.html", errore="Password troppo corta, deve avere almeno 8 caratteri")
    if password != password_confirm:
        return render_template("signin/signin_user.html", errore="Le password non corrispondono")
    if not name or not surname:
        return render_template("signin/signin_user.html", errore="Nome e cognome richiesti")
    
    # Nuovo utente: passenger di default
    new_user = {
        "username": username, 
        "password": password, 
        "email": email,
        "driver": False,
        "name": name,
        "surname": surname,
        "nrTel": "",
        "nrLicense": "",
        "license": ""
    }

    try:
        with open("DataBase/utenti.json", "r", encoding="utf-8") as f:
            try:
                utenti = json.load(f)
            except json.JSONDecodeError:
                utenti = []
    except:
        utenti = []

    # Controlla se username/email già esiste
    for utente in utenti:
        if utente["username"] == username or utente["email"] == email:
            return render_template("signin/signin_user.html", errore="Username o email già registrati")

    utenti.append(new_user)

    with open("DataBase/utenti.json", "w", encoding="utf-8") as f:
        json.dump(utenti, f, ensure_ascii=False, indent=4)

    session["username"] = username
    session["is_driver"] = False

    # Se il form conteneva il flag per diventare driver, reindirizza alla pagina di upgrade
    become_driver = request.form.get('become_driver') or request.args.get('become_driver')
    if become_driver:
        return redirect("/become_driver_page")

    return redirect("/user_dashboard")

# Registrazione driver (aggiunta dati a utente esistente)
@registration_bp.route("/registration_driver")
def registration_driver():
    if "username" not in session:
        return redirect("/login")
    return render_template("signin/signin_driver.html")

@registration_bp.route("/save_driver", methods=["POST"])
def save_driver():
    if "username" not in session:
        return redirect("/login")
    
    username = session["username"]
    nrTel = request.form.get('nrTel', '')
    nrLicense = request.form.get('nrLicense', '')
    license_file = request.files.get('license')
    
    # Validazioni
    if len(nrTel) != 10:
        return render_template("signin/signin_driver.html", errore="Numero di telefono non valido (10 cifre)")
    if len(nrLicense) != 10:
        return render_template("signin/signin_driver.html", errore="Numero di patente non valido (10 caratteri)")
    
    filepath = ""
    if license_file and license_file.content_type.startswith('image/'):
        os.makedirs("app/routes/licenses", exist_ok=True)
        filepath = f"app/routes/licenses/{username}_{nrLicense}"
        license_file.save(filepath)
    
    # Carica utenti e aggiorna
    try:
        with open("DataBase/utenti.json", "r", encoding="utf-8") as f:
            utenti = json.load(f)
    except:
        utenti = []
    
    # Trova e aggiorna l'utente
    for utente in utenti:
        if utente["username"] == username:
            utente["driver"] = True
            utente["nrTel"] = nrTel
            utente["nrLicense"] = nrLicense
            utente["license"] = filepath
            break
    
    with open("DataBase/utenti.json", "w", encoding="utf-8") as f:
        json.dump(utenti, f, ensure_ascii=False, indent=4)
    
    return redirect("/user_dashboard")