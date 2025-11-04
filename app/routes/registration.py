from flask import Blueprint, render_template, redirect

# Per ogni endpoint metto un nome diverso che lo identifica.
registration_bp = Blueprint("registration", __name__)

# Ogni funzione è associata ad un endpoint --> architettura "a progetti".

@registration_bp.route("/registration_driver")
def registration_driver():
    return render_template("login_driver.html")

@registration_bp.route("/registration_passenger")
def registration_passenger():
    return render_template("login_passenger.html")