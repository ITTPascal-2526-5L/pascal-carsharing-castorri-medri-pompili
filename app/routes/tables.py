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