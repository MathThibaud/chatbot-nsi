from flask import Blueprint, request, jsonify
import os
from openai import OpenAI

listes_bp = Blueprint("listes", __name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@listes_bp.route("/ask_listes", methods=["POST"])
def ask_listes():
    data = request.get_json()
    user_input = data.get("message", "").strip().lower()

    with open("nsi_ressources/listes.md", "r", encoding="utf-8") as f:
        reference = f.read()

    if "exercice" in user_input:
        prompt = (
            f"Tu es un assistant pédagogique NSI. "
            f"À partir du document suivant :
{reference}

"
            f"Propose un exercice simple sur les listes, sans solution. "
            f"L'exercice doit être progressif et adapté à un élève de terminale NSI."
        )
    elif "théorie" in user_input or "définition" in user_input:
        prompt = (
            f"Tu es un assistant NSI. Résume brièvement ce qu'est une liste en Python "
            f"à partir du document suivant :
{reference}

"
            f"Utilise un ton clair et accessible."
        )
    elif "def " in user_input or "[" in user_input or "append" in user_input:
        prompt = (
            f"Voici un code soumis par un élève :
{user_input}

"
            f"Analyse, corrige si nécessaire, et explique clairement en t'appuyant sur :
{reference}"
        )
    else:
        prompt = (
            f"Tu es un assistant pédagogique NSI bienveillant. "
            f"Voici ce qu'un élève t'a écrit :
{user_input}

"
            f"Réponds de façon pédagogique, en lien avec les listes Python, en t'appuyant sur :
{reference}"
        )

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant NSI qui aide les élèves en Python. Sois clair, concis et bienveillant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5
        )
        response = completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"❌ Erreur : {e}"}), 500

