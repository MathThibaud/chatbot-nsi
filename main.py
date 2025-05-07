from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import random
import re

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def charger_exercices_md(md_path="sujets_BNS_2025.md"):
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            contenu = f.read()
        sujets = contenu.split("# Sujet ")
        exercices = []
        for sujet in sujets[1:]:
            lignes = sujet.strip().splitlines()
            titre = lignes[0].strip()
            corps = "\n".join(lignes[1:])
            if "EXERCICE 1" in corps and "EXERCICE 2" in corps:
                part1 = corps.split("EXERCICE 1", 1)[1]
                part2_split = part1.split("EXERCICE 2", 1)
                ex1 = "EXERCICE 1\n" + part2_split[0].strip()
                ex2 = "EXERCICE 2\n" + part2_split[1].strip() if len(part2_split) > 1 else "❌ Exercice 2 non trouvé"
                exercices.append((ex1, ex2))
        return exercices
    except Exception as e:
        print("❌ Erreur lecture Markdown :", e)
        return []


@app.route("/get_examen_affichage")
def get_examen_affichage():
    try:
        with open("sujets_affichage.md", "r", encoding="utf-8") as f:
            contenu = f.read()
        sujets = contenu.split("# ✅ Sujet ")
        sujets = [s.strip() for s in sujets if s.strip()]
        sujet = random.choice(sujets)
        return jsonify({"sujet": f"✅ Sujet {sujet}"})
    except Exception as e:
        return jsonify({"sujet": "❌ Erreur lors du chargement du sujet."})


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
            sujets = charger_exercices_md()
            question = sujets[0][0] if sujets else "❌ Aucun exercice disponible."
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
    sujets = charger_exercices_md()
    if not sujets:
        return jsonify({"exercice1": "❌ Exercice 1 introuvable", "exercice2": "❌ Exercice 2 introuvable"})
    sujet = random.choice(sujets)
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
