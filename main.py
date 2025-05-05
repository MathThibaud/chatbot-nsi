from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data["message"]
    file_path = "entrainement_pratique.txt"  # unique fichier de référence

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            document_reference = f.read()
    except FileNotFoundError:
        return jsonify({"response": "❌ Le fichier d'entraînement est introuvable."})

    try:
        if user_input.lower() == "initier":
            prompt = (
                f"Tu es un assistant pédagogique NSI s'adressant à un élève. "
                f"Tu vas t'appuyer strictement sur le document suivant pour poser des questions et analyser les réponses :\n\n"
                f"{document_reference}\n\n"
                f"Commence une session d'entraînement à la pratique des algorithmes du BAC. Pose une première question simple, sans donner la réponse."
            )
        else:
            prompt = (
                f"Tu es un assistant pédagogique NSI s'adressant à un élève. "
                f"Voici le document de référence :\n\n"
                f"{document_reference}\n\n"
                f"Voici ce qu'a répondu l'élève : « {user_input} ». "
                f"Analyse sa réponse, donne un retour directement à l'élève, puis pose une nouvelle question si nécessaire."
            )

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant NSI qui fait travailler un élève sur la pratique des algorithmes. Sois bienveillant, clair, et progressif."
                },
                {"role": "user", "content": prompt}
            ]
        )

        reply = chat_completion.choices[0].message.content.strip()
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"❌ Erreur : {str(e)}"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

