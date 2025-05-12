from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Pages de thèmes (ex: /themes/listes)
@app.route("/themes/<theme>")
def theme_page(theme):
    return render_template(f"themes/{theme}.html")

# Pages d'entraînement et examens
@app.route("/entrainement/<type_entrainement>")
def entrainement(type_entrainement):
    return render_template(f"entrainement/{type_entrainement}.html")

@app.route("/examens/<type_examen>")
def examen(type_examen):
    return render_template(f"examens/{type_examen}.html")

"""
# API pour le chatbot
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": data["message"]}]
    )
    return jsonify({"reply": response.choices[0].message.content})
"""
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    # Personnalisez le prompt selon la page
    prompt = f"Tu es un expert NSI. Réponds à cette question sur {data.get('context', 'Python')}:\n{data['message']}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"reply": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=False)