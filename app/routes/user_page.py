from flask import Blueprint, render_template, redirect, session
import json

user_bp = Blueprint("user", __name__)

@user_bp.route("/user_driver")
def user_driver():
    username = session.get("username")
    return render_template("base_page/base_driver.html", username=username)

@user_bp.route("/user_passenger")
def user_passenger():
    return render_template("base_page/base_passenger.html")