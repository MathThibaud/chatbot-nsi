from flask import Flask

app = Flask(__name__)

def create_app():
    app = Flask(__name__)

    # Importations locales pour éviter les imports circulaires
    from routes.index import index_bp
    from routes.entrainement import entrainement_bp

    # Enregistrement des "blueprints"
    app.register_blueprint(index_bp)
    app.register_blueprint(entrainement_bp)

    return app

from app import routes