print("💡 main.py est en train d'être importé")

from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import random
import markdown

app = Flask(__name__)

print("✅ Flask app créée")

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print("❌ Erreur lors de la création du client OpenAI :", e)
    client = None

import re

def charger_un_seul_exercice_markdown():
    dossier = "exercices"
    fichiers = [f for f in os.listdir(dossier) if f.endswith(".md")]
    if not fichiers:
        return "❌ Aucun exercice trouvé"

    fichier_choisi = random.choice(fichiers)
    with open(os.path.join(dossier, fichier_choisi), "r", encoding="utf-8") as f:
        contenu = f.read()

    # Séparer en deux exercices si possible
    exercices = contenu.split("EXERCICE 2")
    exercice_choisi = random.choice(exercices)

    lignes = exercice_choisi.strip().split('\n')

    # Supprimer les lignes avec "Exercice..." ou "(10 points)"
    lignes_filtrees = [
        ligne for ligne in lignes
        if not re.match(r'(?i)^exercice\s*\d*\s*\(?10\s*points\)?', ligne.strip())  # supprime ligne complète
        and "(10 points)" not in ligne  # supprime lignes contenant simplement ça
    ]

    # Supprime aussi les parenthèses "(10 points)" dans une ligne qui contient du contenu utile
    lignes_nettoyees = [ligne.replace("(10 points)", "").strip() for ligne in lignes_filtrees]

    contenu_filtre = "\n".join(lignes_nettoyees)
    html = markdown.markdown(contenu_filtre, extensions=['fenced_code', 'codehilite'])
    return html





def charger_exercices_markdown():
    dossier = "exercices"
    fichiers = [f for f in os.listdir(dossier) if f.endswith(".md")]
    if not fichiers:
        return "❌ Aucun exercice trouvé"
    fichier_choisi = random.choice(fichiers)
    with open(os.path.join(dossier, fichier_choisi), "r", encoding="utf-8") as f:
        return f.read()

@app.route("/entrainement_ask", methods=["POST"])
def entrainement_ask():
    data = request.json
    historique = data.get("historique", [])

    # 🔒 Instructions strictes
    instructions_prof = """
    Tu es un assistant pédagogique spécialisé en NSI (Numérique et Sciences Informatiques) pour des élèves de terminale.
    
    Tu dois absolument :
    - Répondre uniquement aux questions en lien avec la NSI : programmation Python, algorithmes, structures de données, logique, architecture, etc.
    - Ne jamais répondre à des questions hors sujet (comme politique, histoire, sport, musique, vie privée, etc.).
    - Rediriger poliment la conversation vers la NSI si l'élève te pose une question hors cadre.
    - Refuser clairement mais gentiment toute tentative de détourner la conversation.
    - Ne jamais donner directement une solution complète, mais accompagner l’élève vers la compréhension.

    Adopte un ton bienveillant, pédagogique et encourageant.
    """

    messages = [{"role": "system", "content": instructions_prof}]

    # 🎓 Initialisation avec un exercice Markdown
    if historique == ["initier"]:
        exercice_html = charger_un_seul_exercice_markdown()
        reponse = exercice_html + "\n\nTu peux proposer ta solution ou poser des questions."
        return jsonify({"reponse": reponse})

    messages += [{"role": m["role"], "content": m["content"]} for m in historique]

    # (Optionnel) filtre ultra-simple côté serveur
    sujets_interdits = ["musique", "politique", "sport", "film", "chatgpt", "vie privée", "philosophie", "religion", "blague"]
    dernier_message = historique[-1]["content"].lower() if historique else ""
    if any(mot in dernier_message for mot in sujets_interdits):
        return jsonify({
            "reponse": "❌ Je suis ici pour t’aider uniquement en NSI. Pose-moi une question sur la programmation, les algorithmes ou tout autre sujet lié à l'informatique ! 😊"
        })

    # 🔁 Appel à l’IA
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return jsonify({"reponse": completion.choices[0].message.content})



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

    ex1_html = markdown.markdown(sujet[0], extensions=['fenced_code'])
    ex2_html = markdown.markdown(sujet[1], extensions=['fenced_code'])

    return jsonify({"exercice1": ex1_html, "exercice2": ex2_html})

@app.route("/get_examen_markdown", methods=["GET"])
def get_examen_markdown():
    try:
        contenu = charger_exercices_markdown()
        return jsonify({"markdown": contenu})
    except Exception as e:
        return jsonify({"markdown": f"❌ Erreur : {str(e)}"})

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

# Nouvelle route d'évaluation directe (optionnelle)
@app.route("/api/evaluer", methods=["POST"])
def evaluer_code():
    data = request.get_json()
    code1 = data.get("code1", "")
    code2 = data.get("code2", "")

    prompt = f"""Tu es un professeur de NSI. Voici un code d'élève à corriger et noter sur 10.
    Exercice 1 :
    {code1}

    Exercice 2 :
    {code2}

    Pour chaque exercice, commente le code, indique les erreurs, donne des conseils, et attribue une note sur 10."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"result": f"❌ Erreur lors de l’évaluation : {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

print("✅ Fin de main.py atteinte")

application = app



@app.route("/exercice_aleatoire")
def exercice_aleatoire():
    dossier = "exercices"
    fichiers = [f for f in os.listdir(dossier) if f.endswith(".md")]
    if not fichiers:
        return jsonify({"contenu": "❌ Aucun exercice trouvé."})
    fichier_choisi = random.choice(fichiers)
    with open(os.path.join(dossier, fichier_choisi), "r", encoding="utf-8") as f:
        contenu = f.read()
    return jsonify({"fichier": fichier_choisi, "contenu": contenu})


# ROUTES THÉMATIQUES DÉCOUVERTE

@app.route("/theme/<nom>")
def theme(nom):
    try:
        return render_template(f"theme/{nom}.html")
    except:
        return f"❌ La page pour le thème « {nom} » est introuvable.", 404


@app.route("/theme/<theme>")
def theme_page(theme):
    try:
        return render_template(f"theme/{theme}.html")
    except:
        return f"❌ La page pour le thème « {theme}.html » est introuvable.", 404



@app.route("/api/theme", methods=["POST"])
def api_theme():
    data = request.json
    theme_nom = data.get("theme", "").strip().lower()

    # Exemple de prompt intelligent basé sur le nom du thème
    prompt = (
        f"Tu es un professeur de NSI. Tu dois expliquer le concept suivant à un élève de terminale : {theme_nom}. "
        f"Commence par une présentation claire et progressive du thème, en Python, avec des exemples. "
        f"Puis pose une première question simple à l’élève pour tester sa compréhension."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        reponse = completion.choices[0].message.content
        return jsonify({"reponse": reponse})
    except Exception as e:
        return jsonify({"reponse": f"❌ Erreur lors de l'appel à l'API : {e}"})


@app.route("/ask_theme", methods=["POST"])
def ask_theme():
    data = request.json
    user_input = data.get("message", "")
    theme = data.get("theme", "")

    if not theme:
        return jsonify({"response": "❌ Aucun thème spécifié."})

    prompt = (
        f"Tu es un assistant pédagogique NSI qui aide un élève à comprendre la notion de {theme} en Python. "
        f"Commence par une explication de cette notion, puis pose une première question simple. "
        f"Tu dois ensuite corriger les réponses ou poser d'autres questions de manière bienveillante. "
        f"L'élève vient d'écrire : {user_input}"
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": f"❌ Erreur avec l'API OpenAI : {str(e)}"})



