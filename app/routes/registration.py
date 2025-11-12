from flask import Blueprint, render_template, redirect, request
import json

# Per ogni endpoint metto un nome diverso che lo identifica.
registration_bp = Blueprint("registration", __name__)

# Ogni funzione è associata ad un endpoint --> architettura "a progetti".

@registration_bp.route("/registration_driver")
def registration_driver():
    return render_template("signin/signin_driver.html")

@registration_bp.route("/save_driver", methods=["POST"])
def save_driver():
    username = request.form['username']
    email = request.form['email']
    if email.Contains("@") == False:
        return render_template("signin/signin_driver.html", errore="Email non valida")
    
    nrTel = request.form['nrTel']
    if len(nrTel) != 10:
        return render_template("signin/signin_driver.html", errore="Numero di telefono non valido")
    
    password = request.form['password']
    if len(password) < 8:
        return render_template("signin/signin_driver.html", errore="Password troppo corta, deve avere almeno 8 caratteri")
    
    nrPatente = request.form['nrPatente']
    if len(nrPatente) != 10:
        return render_template("signin/signin_driver.html", errore="Numero di patente non valido")

    new_driver = {
        "username": username, 
        "password": password, 
        "email": email, 
        "nrTel": nrTel, 
        "nrPatente": nrPatente
    }

    try:
        with open("drivers.json", "r", encoding="utf-8") as f:
            try:
                drivers = json.load(f)
            except json.JSONDecodeError:
                drivers = []
    except:
        drivers = []

    drivers.append(new_driver)

    with open("drivers.json", "w", encoding="utf-8") as f:
        json.dump(drivers, f, ensure_ascii=False, indent=4)

    return render_template("signin/signin_driver.html", messaggio="Salvataggio eseguito con successo!")
    # return redirect(/driver)

@registration_bp.route("/registration_passenger")
def registration_passenger():
    return render_template("signin/signin_passenger.html")

@registration_bp.route("/save_passenger", methods=["POST"])
def save_passenger():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    if "@" not in email:
        return render_template("signin/signin_passenger.html", errore="Email non valida")

    if len(password) < 8:
        return render_template("signin/signin_passenger.html", errore="Password troppo corta, deve avere almeno 8 caratteri")

    new_passenger = {
        "username": username, 
        "password": password, 
        "email": email
    }

    try:
        with open("passengers.json", "r", encoding="utf-8") as f:
            try:
                passengers = json.load(f)
            except json.JSONDecodeError:
                passengers = []
    except:
        passengers = []

    passengers.append(new_passenger)

    with open("passengers.json", "w", encoding="utf-8") as f:
        json.dump(passengers, f, ensure_ascii=False, indent=4)

    return render_template("signin/signin_passenger.html", messaggio="Salvataggio eseguito con successo!")
    # return redirect(/driver)

# registrazione del driver, quando si clicca submit i dati si salvano in un file txt, json (consigliato) o xml
# relativa registrazione del veicolo (magari nella pagina del driver)
# solo dati
# registrazione passenger 
# registrazione scuole