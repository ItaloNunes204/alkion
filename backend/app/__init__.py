from flask import Flask
from dotenv import load_dotenv

from .core.config import config_by_name
from .core.extensions import db, migrate, jwt, redis_client
from .core.exceptions import register_error_handlers
from .core.middleware import register_middlewares

load_dotenv()

def create_app(config_name: str = "development") -> Flask:

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    redis_client.init_app(app)

    register_error_handlers(app)
    register_middlewares(app)

    _register_blueprints(app)

    return app


def _register_blueprints(app: Flask):
    from .modules.auth.routes import auth_bp
    from .modules.sync.routes import sync_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(sync_bp, url_prefix="/api/v1/sync")
