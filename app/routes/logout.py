from flask import Blueprint, render_template, session

logout_bp = Blueprint("logout", __name__)

@logout_bp.route("/logout")
# Cancella tutti i dati presenti nella sessione.
def logout():
    session.clear()
    return render_template("home_page.html")