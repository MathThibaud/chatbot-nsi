from flask import Blueprint, render_template

bp_entrainement = Blueprint("entrainement", __name__)

@bp_entrainement.route("/entrainement")
def entrainement():
    return render_template("entrainement.html")
