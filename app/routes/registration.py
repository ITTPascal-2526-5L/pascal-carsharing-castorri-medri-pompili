from flask import Blueprint, render_template, redirect

# Per ogni endpoint metto un nome diverso che lo identifica.
registration_bp = Blueprint("registration", __name__)

# Ogni funzione è associata ad un endpoint --> architettura "a progetti".

@registration_bp.route("/registration_driver")
def registration_driver():
    return render_template("login/login_driver.html")

@registration_bp.route("/registration_passenger")
def registration_passenger():
    return render_template("login/login_passenger.html")

# registrazione del driver, quando si clicca submit i dati si salvano in un file txt, json (consigliato) o xml
# relativa registrazione del veicolo (magari nella pagina del driver)
# solo dati
# registrazione passenger 
# registrazione scuole