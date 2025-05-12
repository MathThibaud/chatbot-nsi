from flask import Flask, render_template, request, jsonify
import os
import markdown
import random
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return "✅ Application Flask opérationnelle"

# ajoute ici tes autres routes
