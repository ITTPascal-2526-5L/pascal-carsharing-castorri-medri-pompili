from flask import Blueprint, render_template, redirect, request, session
import json
import os

vehicles_bp = Blueprint("vehicles", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "DataBase")
os.makedirs(db_path, exist_ok=True)

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

    vehicles_file = os.path.join(db_path, "vehicles.json")

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
        with open(vehicles_file, "r", encoding="utf-8") as f:
            try:
                vehicles = json.load(f)
            except json.JSONDecodeError:
                vehicles = {}
    except:
        vehicles = {}

    vehicles.setdefault(username, []).append(new_vehicle)

    with open(vehicles_file, "w", encoding="utf-8") as f:
        json.dump(vehicles, f, ensure_ascii=False, indent=4)

    # Ricorda: una volta creato il template che mostra le macchine del driver collegarsi a quello 
    return redirect("/user_driver")