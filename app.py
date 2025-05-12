from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Application Flask déployée avec succès sur Clever Cloud !"
