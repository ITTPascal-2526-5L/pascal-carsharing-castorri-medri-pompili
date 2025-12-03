from flask import Blueprint, render_template, redirect, request, session, flash
import json

login_bp = Blueprint("login", __name__)

@login_bp.route("/login")
def new_login():
    return render_template("login/login.html")
    
@login_bp.route("/check_login", methods=["POST"])
def check_login():
    username = request.form['username']
    password = request.form['password']

    checkin = False

    try:
        with open("DataBase/drivers.json", "r", encoding="utf-8") as f:
            drivers = json.load(f)

            for driver in drivers:
                if (driver["username"] == username or driver["email"] == username) and driver["password"] == password:
                    session["username"] = driver["username"]
                    checkin = True
            
        if checkin:
            return redirect("/user_driver")
        else:
            flash("Credenziali errate", "danger")
            return render_template("login/login.html")
    except:
        flash("Credenziali errate", "danger")
        return render_template("login/login.html")