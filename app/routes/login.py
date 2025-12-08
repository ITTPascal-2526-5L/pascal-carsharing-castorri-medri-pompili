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

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_pathdb = os.path.join(BASE_DIR, "All_Users")
    os.makedirs(db_pathdb, exist_ok=True)

    users_file = os.path.join(db_pathdb, "users.json")

    try:
        with open(users_file, "r", encoding="utf-8") as f:
            users = json.load(f)

            for user in users:
                if (user["username"] == username or user["email"] == username) and user["password"] == password:
                    session["username"] = user["username"]
                    session["is_driver"] = user.get("driver", False)
                    return redirect("/user_dashboard")
            
            flash("Credenziali errate", "danger")
            return render_template("login/login.html")
    except:
        flash("Errore nel login", "danger")
        return render_template("login/login.html")

@login_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Logout effettuato", "success")
    return redirect("/")