from flask import Blueprint, render_template
import json

tables_bp = Blueprint("tables", __name__)

@tables_bp.route("/drivers_detail")
def drivers_detail():
    try:
        with open("DataBase/drivers.json", "r", encoding="utf-8")as f:
            data = json.load(f)
        return render_template("tables/drivers_detail.html", drivers=data, message="")
    except: 
        return render_template("tables/drivers_detail.html", message="No drivers saved.")
    
@tables_bp.route("/passengers_detail")
def passengers_detail():
    try:
        with open("DataBase/passengers.json", "r", encoding="utf-8")as f:
            data = json.load(f)
        return render_template("tables/passengers_detail.html", passengers=data, message="")
    except: 
        return render_template("tables/passengers_detail.html", message="No passengers saved.")
    
@tables_bp.route("/schools_detail")
def schools_detail():
    try:
        with open("DataBase/schools.json", "r", encoding="utf-8")as f:
            data = json.load(f)
        return render_template("tables/schools_detail.html", schools=data, message="")
    except: 
        return render_template("tables/schools_detail.html", message="No schools saved.")