
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import random
import fitz  # PyMuPDF
import re

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extraire_exercices_du_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        raw_pages = [page.get_text() for page in doc]
        sujets = []
        i = 0

        while i < len(raw_pages):
            page = raw_pages[i]
            match_debut = re.search(r"1\s*/\s*(\d)", page)
            if match_debut:
                n = int(match_debut.group(1))
                bloc = raw_pages[i:i + n] if i + n <= len(raw_pages) else raw_pages[i:]
                # Supprimer les repères de pagination *après* avoir détecté le bloc
                bloc_nettoye = [re.sub(r"\b\d+\s*/\s*\d+\b", "", p) for p in bloc]
                texte_complet = "\n".join(bloc_nettoye)
                if "EXERCICE 1" in texte_complet and "EXERCICE 2" in texte_complet:
                    partie1 = texte_complet.split("EXERCICE 1", 1)[1]
                    partie2 = partie1.split("EXERCICE 2", 1)
                    ex1 = "EXERCICE 1\n" + partie2[0].strip()
                    ex2 = "EXERCICE 2\n" + partie2[1].strip() if len(partie2) > 1 else "❌ Exercice 2 non trouvé"
                    sujets.append((ex1, ex2))
                i += n
            else:
                i += 1
        print(f"✅ {len(sujets)} sujets détectés dans le PDF")
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

