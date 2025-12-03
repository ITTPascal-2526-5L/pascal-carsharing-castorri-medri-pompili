from flask import Blueprint, render_template, redirect, session
import json

user_bp = Blueprint("user", __name__)

@user_bp.route("/user_driver")
def user_driver():
    # Se esistono i valori all'interno della sessione.
    if 'username' in session.keys():
        username = session.get("username")
        return render_template("base_page/base_driver.html", username=username)
    else:
        return "No session data found"

@user_bp.route("/user_passenger")
def user_passenger():
    return render_template("base_page/base_passenger.html")