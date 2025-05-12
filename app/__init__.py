# app/__init__.py
from flask import Flask
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_app():
    app = Flask(__name__)

    from .routes_entrainement import entrainement_bp
    from .routes_examen import examen_bp
    from .routes_theme import theme_bp

    app.register_blueprint(entrainement_bp)
    app.register_blueprint(examen_bp)
    app.register_blueprint(theme_bp)

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    return app
