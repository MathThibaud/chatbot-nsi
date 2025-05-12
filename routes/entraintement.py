from flask import Blueprint, render_template

index_bp = Blueprint("entrainement", __name__)

@index_bp.route("/")
def index():
    return render_template("entrainement.html")