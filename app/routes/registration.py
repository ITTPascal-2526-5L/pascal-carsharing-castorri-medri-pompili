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
    nrTel = request.form['nrTel']
    nrLicense = request.form['nrLicense']
    license = request.files.get('license')

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_pathdb = os.path.join(BASE_DIR, "DataBase")
    os.makedirs(db_pathdb, exist_ok=True)

    drivers_file = os.path.join(db_pathdb, "drivers.json")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "licenses")
    os.makedirs(db_path, exist_ok=True)

    # salvo la patete dentro la cartella "licenses"
    # il nome del file è nel formato username_numeroPatente
    if license.content_type.startswith('image/'):
        filepath = os.path.join(db_path, f"{username}_{nrLicense}")
        license.save(filepath)

    new_driver = {
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
        # "r" --> sola lettura
        # "w" --> se non esiste lo crea da zero
        with open(drivers_file, "r", encoding="utf-8") as f:
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

    with open(drivers_file, "w", encoding="utf-8") as f:
        json.dump(drivers, f, ensure_ascii=False, indent=4)

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

@registration_bp.route("/save_passenger", methods=["POST"])
def save_passenger():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    new_passenger = {
        "username": username, 
        "password": password, 
        "email": email
    }

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "DataBase")
    os.makedirs(db_path, exist_ok=True)

    passengers_file = os.path.join(db_path, "passengers.json")

    try:
        with open(passengers_file, "r", encoding="utf-8") as f:
            try:
                passengers = json.load(f)
            except json.JSONDecodeError:
                passengers = []
    except:
        passengers = []

    passengers.append(new_passenger)

    with open(passengers_file, "w", encoding="utf-8") as f:
        json.dump(passengers, f, ensure_ascii=False, indent=4)

    return "Salvataggio eseguito con successo!"