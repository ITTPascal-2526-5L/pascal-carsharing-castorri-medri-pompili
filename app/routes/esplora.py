from flask import Blueprint, render_template
import json

esplora_bp = Blueprint("esplora", __name__)

@esplora_bp.route("/esplora_drivers")
def esplora_drivers():
    try:
        with open("DataBase/drivers.json", "r", encoding="utf-8")as f:
            data = json.load(f)
        return render_template("esplora/esplora_drivers.html", drivers=data, message="")
    except: 
        return render_template("esplora/esplora_drivers.html", message="No drivers.")