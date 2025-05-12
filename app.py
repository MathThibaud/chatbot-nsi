from flask import Flask

application = Flask(__name__)

@aapplication.route("/")
def index():
    return "✅ Application Flask déployée avec succès sur CleverCloud !"
