from flask import Blueprint, request, jsonify
import os
import openai

listes_bp = Blueprint("listes", __name__)

# Configuration de l'API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@listes_bp.route("/ask_listes", methods=["POST"])
def ask_listes():
    data = request.get_json()
    user_input = data.get("message", "").strip().lower()

    try:
        with open("nsi_ressources/listes.md", "r", encoding="utf-8") as f:
            reference = f.read()
    except FileNotFoundError:
        return jsonify({"response": "❌ Le fichier listes.md est introuvable."})

    if "exercice" in user_input:
        prompt = (
            f"Tu es un assistant pédagogique NSI. "
            f"À partir du document suivant :\n{reference}\n\n"
            f"Propose un exercice simple sur les listes, sans solution. "
            f"L'exercice doit être progressif et adapté à un élève de terminale NSI."
        )
    elif "théorie" in user_input or "définition" in user_input:
        prompt = (
            f"Tu es un assistant NSI. "
            f"À partir du document suivant :\n{reference}\n\n"
            f"Explique de manière claire et synthétique les principales notions à connaître sur les listes en Python."
        )
    else:
        prompt = (
            f"Tu es un assistant pédagogique NSI. "
            f"Voici un extrait de cours :\n{reference}\n\n"
            f"En t'appuyant sur ce contenu, répond à la question suivante :\n{user_input}"
        )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": f"❌ Erreur OpenAI : {e}"})
