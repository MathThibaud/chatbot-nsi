from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI
import os

listes_bp = Blueprint('listes', __name__, url_prefix='/themes/listes')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



@listes_bp.route('/')
def listes_home():
    return render_template('themes/listes.html')

@listes_bp.route('/chat', methods=['POST'])
def chat_listes():
    user_message = request.json.get('message')
    
    # Charger le contexte spécifique aux listes
    with open('nsi_ressources/listes.md', 'r') as f:
        contexte = f.read()
    
    prompt = f"""
    Tu es un assistant pédagogique spécialisé en NSI sur le thème des listes Python.
    Contexte officiel NSI:
    {contexte}
    
    Message de l'élève: {user_message}
    
    Réponds de manière pédagogique en:
    1. Identifiant si c'est une question de code ou de théorie
    2. Donnant des exemples concrets
    3. Proposant des exercices si l'élève semble prêt
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return jsonify({"response": response.choices[0].message.content})