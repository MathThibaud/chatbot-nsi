from . import app

@app.route("/")
def index():
    return "Application Flask fonctionnelle"
