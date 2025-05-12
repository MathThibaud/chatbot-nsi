# app/routes_examen.py
from flask import Blueprint, render_template, jsonify, request
import random
import os

examen_bp = Blueprint("examen", __name__)

@examen_bp.route("/examen")
def examen():
    return render_template("examen.html")

@examen_bp.route("/exercice_aleatoire")
def exercice_aleatoire():
    fichiers = [f for f in os.listdir("exercices") if f.endswith(".md")]
    if not fichiers:
        return jsonify({"contenu": "❌ Aucun fichier trouvé"})
    choisi = random.choice(fichiers)
    with open(os.path.join("exercices", choisi), encoding="utf-8") as f:
        return jsonify({"contenu": f.read()})

@examen_bp.route("/evaluer", methods=["POST"])
def evaluer():
    data = request.get_json()
    code1 = data.get("code1", "")
    code2 = data.get("code2", "")
    return jsonify({"resultat": "✅ Code reçu.\n\n[Ce bloc pourra être remplacé par une vraie évaluation automatique]."})
