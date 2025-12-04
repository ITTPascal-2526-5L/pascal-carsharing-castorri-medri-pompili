from flask import Blueprint, render_template
import json
import os

tables_bp = Blueprint("tables", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "DataBase")
os.makedirs(db_path, exist_ok=True)

@tables_bp.route("/drivers_detail")
def drivers_detail():
    drivers_file = os.path.join(db_path, "drivers.json")
    try:
        with open(drivers_file, "r", encoding="utf-8")as f:
            data = json.load(f)
        return render_template("tables/drivers_detail.html", drivers=data, message="")
    except: 
        return render_template("tables/drivers_detail.html", message="No drivers saved.")
    
@tables_bp.route("/passengers_detail")
def passengers_detail():
    passengers_file = os.path.join(db_path, "passengers.json")
    try:
        with open(passengers_file, "r", encoding="utf-8")as f:
            data = json.load(f)
        return render_template("tables/passengers_detail.html", passengers=data, message="")
    except: 
        return render_template("tables/passengers_detail.html", message="No passengers saved.")
    
@tables_bp.route("/schools_detail")
def schools_detail():
    schools_file = os.path.join(db_path, "schools.json")

    try:
        with open(schools_file, "r", encoding="utf-8")as f:
            data = json.load(f)
        return render_template("tables/schools_detail.html", schools=data, message="")
    except: 
        return render_template("tables/schools_detail.html", message="No schools saved.")