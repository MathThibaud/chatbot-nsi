from .route_listes import listes_bp

# Liste de tous les blueprints à exporter
__all__ = ['listes_bp']

# Initialisation optionnelle (si besoin)
def init_app(app):
    """Fonction pour enregistrer les blueprints avec l'application Flask"""
    app.register_blueprint(listes_bp)
    # Ajouter d'autres blueprints ici au fur et à mesure