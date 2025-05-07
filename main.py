
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import random
import fitz  # PyMuPDF

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extraire_exercices_du_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        pages = [page.get_text() for page in doc]  # conserve les 

        sujets = []
        i = 0
        while i < len(pages):
            page = pages[i]
            if "EXERCICE 1" in page:
                ex1 = ""
                ex2 = ""
                # Récupérer pages de l'exercice 1
                while i < len(pages) and "EXERCICE 2" not in pages[i]:
                    ex1 += "\n" + pages[i]
                    i += 1
                # Récupérer pages de l'exercice 2
                while i < len(pages) and ("EXERCICE 1" not in pages[i] or "EXERCICE 2" in pages[i]):
                    ex2 += "\n" + pages[i]
                    i += 1
                # Nettoyage
                ex1_txt = ex1.split("EXERCICE 1", 1)[1].strip() if "EXERCICE 1" in ex1 else ex1.strip()
                ex2_txt = ex2.split("EXERCICE 2", 1)[1].strip() if "EXERCICE 2" in ex2 else ex2.strip()
                sujets.append(("EXERCICE 1\n" + ex1_txt, "EXERCICE 2\n" + ex2_txt))
            else:
                i += 1
        return sujets
    except Exception as e:
        print("❌ Erreur d’extraction PDF :", e)
        return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/entrainement")
def entrainement():
    return render_template("entrainement.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data["message"]
    file_path = "entrainement_pratique.txt"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            document_reference = f.read()
    except FileNotFoundError:
        return jsonify({"response": "❌ Le fichier d'entraînement est introuvable."})

    try:
        if user_input.lower() == "initier":
            exercices = extraire_exercices_du_pdf("static/pdf/BNS_2025_pdf_unique.pdf")
            question = exercices[0][0] if exercices else "❌ Aucun exercice disponible."
            prompt = (
                f"{document_reference}\n\n"
                f"Voici un exercice extrait du sujet officiel :\n{question}\n"
                f"Ne donne pas la réponse. Attends celle de l'élève."
            )
        else:
            prompt = (
                f"{document_reference}\n\n"
                f"Voici ce qu'a répondu l'élève : « {user_input} ». "
                f"Analyse sa réponse, donne un retour directement à l'élève, puis pose une nouvelle question si nécessaire."
            )

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant NSI qui fait travailler un élève sur la pratique des algorithmes. Sois bienveillant, clair, et progressif."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = chat_completion.choices[0].message.content.strip()
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"❌ Erreur : {str(e)}"})

@app.route("/examen")
def examen():
    return render_template("examen.html")

@app.route("/get_examen", methods=["GET"])
def get_examen():
    exercices = extraire_exercices_du_pdf("static/pdf/BNS_2025_pdf_unique.pdf")
    if not exercices:
        return jsonify({"exercice1": "❌ Exercice 1 introuvable", "exercice2": "❌ Exercice 2 introuvable"})
    sujet = random.choice(exercices)
    return jsonify({"exercice1": sujet[0], "exercice2": sujet[1]})

@app.route("/correction-examen", methods=["POST"])
def correction_examen():
    data = request.json
    rep1 = data.get("reponse1", "").strip()
    rep2 = data.get("reponse2", "").strip()

    try:
        with open("entrainement_pratique.txt", "r", encoding="utf-8") as f:
            document_reference = f.read()
    except FileNotFoundError:
        return jsonify({"response": "❌ Le fichier d'entraînement est introuvable."})

    prompt = (
        f"{document_reference}\n\n"
        f"L'élève vient de terminer un examen blanc.\n"
        f"Voici sa réponse à l'exercice 1 :\n{rep1}\n\n"
        f"Et sa réponse à l'exercice 2 :\n{rep2}\n\n"
        f"Corrige ces deux réponses, indique les erreurs éventuelles, propose des améliorations. "
        f"Donne ensuite une note globale sur 20 avec des commentaires pédagogiques motivants."
    )

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un correcteur bienveillant pour un examen blanc de NSI. Sois clair, rigoureux, encourageant et juste."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = chat_completion.choices[0].message.content.strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"❌ Erreur : {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
