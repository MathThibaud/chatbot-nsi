from flask import Flask

app = Flask(__name__)


def create_app():
    app = Flask(__name__)

    from .routes.index import bp_index
    from .routes.entrainement import bp_entrainement

    app.register_blueprint(bp_index)
    app.register_blueprint(bp_entrainement)

    return app
