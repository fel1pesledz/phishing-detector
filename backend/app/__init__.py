from flask import Flask

from app.routes.health import bp as health_bp
from app.routes.scan import bp as scan_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(health_bp)
    app.register_blueprint(scan_bp)
    return app
