from flask import Blueprint, render_template, redirect, request, session
import json

vehicles_bp = Blueprint("vehicles", __name__)

@vehicles_bp.route("/vehicles", methods=["POST"])
def new_vehicles():
    targa = request.form['targa']
    modello = request.form['modello']
    capienza = request.form['capienza']
    anno = request.form['anno']
    username = session["username"]

    new_vehicle = {
        "targa": targa, 
        "modello": modello, 
        "capienza": capienza, 
        "anno": anno,
    }

    try:
        with open("vehicles.json", "r", encoding="utf-8") as f:
            try:
                vehicles = json.load(f)
            except json.JSONDecodeError:
                vehicles = {}
    except:
        vehicles = {}

    vehicles.setdefault(username, []).append(new_vehicle)

    with open("vehicles.json", "w", encoding="utf-8") as f:
        json.dump(vehicles, f, ensure_ascii=False, indent=4)

    return "Salvataggio eseguito con successo!"
    # return redirect(/driver)