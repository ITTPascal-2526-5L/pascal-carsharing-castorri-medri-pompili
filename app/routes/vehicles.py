from flask import Blueprint, render_template, redirect, request, session
import json

vehicles_bp = Blueprint("vehicles", __name__)

@vehicles_bp.route("/add_vehicles")
def add_vehicles():
    return render_template("car.html")

@vehicles_bp.route("/new_vehicles", methods=["POST"])
def new_vehicles():
    marca = request.form['marca'].capitalize()
    modello = request.form['modello'].capitalize()
    targa = request.form['targa'].upper()
    capienza = request.form['capienza']
    carburante = request.form['carburante']
    colore = request.form['colore'].capitalize()
    potenza = request.form['potenza']
    username = session["username"]

    new_vehicle = {
        "marca": marca, 
        "modello": modello, 
        "targa": targa,
        "capienza": capienza,
        "carburante": carburante,
        "colore": colore,
        "potenza": potenza
    }

    try:
        with open("DataBase/vehicles.json", "r", encoding="utf-8") as f:
            try:
                vehicles = json.load(f)
            except json.JSONDecodeError:
                vehicles = {}
    except:
        vehicles = {}

    vehicles.setdefault(username, []).append(new_vehicle)

    with open("DataBase/vehicles.json", "w", encoding="utf-8") as f:
        json.dump(vehicles, f, ensure_ascii=False, indent=4)

    # Dopo aver salvato il veicolo, torniamo al dashboard utente
    return redirect("/user_dashboard")