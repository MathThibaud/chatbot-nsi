# app/routes_theme.py
from flask import Blueprint, render_template, request, jsonify
from . import client

theme_bp = Blueprint("theme", __name__)

@theme_bp.route("/theme/<theme>")
def theme_page(theme):
    return render_template(f"{theme}.html", theme=theme)

@theme_bp.route("/ask_theme", methods=["POST"])
def ask_theme():
    data = request.get_json()
    theme = data.get("theme")
    message = data.get("message", "initier")

    try:
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Thème : {theme}\n{message}"}]
        )
        return jsonify({"response": chat.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": f"❌ Erreur IA : {e}"})
