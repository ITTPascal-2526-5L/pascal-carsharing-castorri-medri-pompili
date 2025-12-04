from flask import Blueprint, render_template, redirect, request, session, flash
import json
import os

login_bp = Blueprint("login", __name__)

@login_bp.route("/login")
def new_login():
    return render_template("login/login.html")
    
@login_bp.route("/check_login", methods=["POST"])
def check_login():
    username = request.form['username']
    password = request.form['password']

    checkin = False

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_pathdb = os.path.join(BASE_DIR, "DataBase")
    os.makedirs(db_pathdb, exist_ok=True)

    drivers_file = os.path.join(db_pathdb, "drivers.json")

    try:
        with open(drivers_file, "r", encoding="utf-8") as f:
            drivers = json.load(f)

            for utente in utenti:
                if (utente["username"] == username or utente["email"] == username) and utente["password"] == password:
                    session["username"] = utente["username"]
                    session["is_driver"] = utente.get("driver", False)
                    return redirect("/user_dashboard")
            
            flash("Credenziali errate", "danger")
            return render_template("login/login.html")
    except Exception as e:
        flash("Errore nel login", "danger")
        return render_template("login/login.html")

@login_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Logout effettuato", "success")
    return redirect("/")