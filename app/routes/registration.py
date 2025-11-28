from flask import Blueprint, render_template, redirect, request, session
import json
import os

# Per ogni endpoint metto un nome diverso che lo identifica.
registration_bp = Blueprint("registration", __name__)

# Ogni funzione è associata ad un endpoint --> architettura "a progetti".

@registration_bp.route("/registration_driver")
def registration_driver():
    return render_template("signin/signin_driver.html")

@registration_bp.route("/save_driver", methods=["POST"])
def save_driver():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    nrTel = request.form['nrTel']
    nrLicense = request.form['nrLicense']
    license = request.files.get('license')

    # salvo la patete dentro la cartella "licenses"
    # il nome del file è nel formato username_numeroPatente
    if license.content_type.startswith('image/'):
        filepath = os.path.join("licenses", f"{username}_{nrLicense}")
        license.save(filepath)

    new_driver = {
        "username": username, 
        "password": password, 
        "email": email, 
        "nrTel": nrTel,
        "nrLicense": nrLicense,
        "license": filepath
    }

    try:
        # "r" --> sola lettura
        # "w" --> se non esiste lo crea da zero
        with open("DataBase/drivers.json", "r", encoding="utf-8") as f:
            try:
                drivers = json.load(f)
            except json.JSONDecodeError:
                drivers = []
    except:
        drivers = []

    drivers.append(new_driver)

    with open("DataBase/drivers.json", "w", encoding="utf-8") as f:
        json.dump(drivers, f, ensure_ascii=False, indent=4)

    session["username"] = username

    return redirect("/user_driver")

@registration_bp.route("/registration_passenger")
def registration_passenger():
    return render_template("signin/signin_passenger.html")

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

    try:
        with open("DataBase/passengers.json", "r", encoding="utf-8") as f:
            try:
                passengers = json.load(f)
            except json.JSONDecodeError:
                passengers = []
    except:
        passengers = []

    passengers.append(new_passenger)

    with open("DataBase/passengers.json", "w", encoding="utf-8") as f:
        json.dump(passengers, f, ensure_ascii=False, indent=4)

    return "Salvataggio eseguito con successo!"