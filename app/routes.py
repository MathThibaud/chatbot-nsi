from flask import render_template, request, jsonify
from app import app
from .openai_helper import get_openai_response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    response = get_openai_response(user_message)
    return jsonify({'response': response})