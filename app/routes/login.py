from flask import Blueprint, render_template, redirect

login_bp = Blueprint("login", __name__)

@login_bp.route("/login")
def new_login():
    return render_template("login/login.html")