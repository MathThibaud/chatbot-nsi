# app/routes_entrainement.py
from flask import Blueprint, request, jsonify, render_template
from . import client

entrainement_bp = Blueprint("entrainement", __name__)

@entrainement_bp.route("/entrainement")
def entrainement():
    return render_template("entrainement.html")

@entrainement_bp.route("/entrainement_ask", methods=["POST"])
def entrainement_ask():
    data = request.get_json()
    historique = data.get("historique", [])

    try:
        messages = []
        for msg in historique:
            if isinstance(msg, str):  # cas "initier"
                messages.append({"role": "user", "content": msg})
            else:
                messages.append(msg)

        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return jsonify({"reponse": chat.choices[0].message.content})

    except Exception as e:
        return jsonify({"reponse": f"❌ Erreur IA : {e}"})
