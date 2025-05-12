# app/utils.py
import os
import random

def charger_exercices_markdown():
    dossier = "exercices"
    fichiers = [f for f in os.listdir(dossier) if f.endswith(".md")]
    if not fichiers:
        return "❌ Aucun exercice trouvé"
    fichier_choisi = random.choice(fichiers)
    with open(os.path.join(dossier, fichier_choisi), "r", encoding="utf-8") as f:
        return f.read()
