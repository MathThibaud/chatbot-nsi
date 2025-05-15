from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI
import os
from datetime import datetime

listes_bp = Blueprint('listes', __name__, url_prefix='/themes/listes')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@listes_bp.route('/')
def listes_home():
    return render_template('themes/listes.html', now=datetime.now().strftime("%H:%M"))

@listes_bp.route('/chat', methods=['POST'])
def chat_listes():
    data = request.json
    user_message = data.get('message')
    is_code = data.get('is_code', False)
    
    # Charger le contexte
    with open('nsi_ressources/listes.md', 'r') as f:
        contexte = f.read()
    
    # Adapter le prompt selon le type
    if is_code:
        prompt = f"""
        Tu es un expert Python spécialisé dans l'enseignement des listes.
        Voici du code d'un élève à corriger :
        {user_message}
        
        Conseils :
        1. Identifie d'abord si le code fonctionne
        2. Propose une correction si nécessaire
        3. Explique les erreurs de manière pédagogique
        4. Propose un exercice similaire
        """
    else:
        prompt = f"""
        Tu es un professeur de NSI expliquant les listes en Python.
        Question de l'élève : {user_message}
        
        Réponds en :
        1. Donnant une explication claire
        2. Fournissant un exemple de code
        3. Proposant un exercice pratique
        """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": contexte},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return jsonify({"response": response.choices[0].message.content})