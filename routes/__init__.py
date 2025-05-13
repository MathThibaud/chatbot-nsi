from .route_listes import listes_bp
__all__ = ['listes_bp']

def init_app(app):
    # Initialisation des routes ici
    from .route_listes import listes_bp
    app.register_blueprint(listes_bp)