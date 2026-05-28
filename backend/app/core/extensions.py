from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis

db           = SQLAlchemy()
migrate      = Migrate()
jwt          = JWTManager()
redis_client = FlaskRedis()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    try:
        token_in_redis = redis_client.get(f"blocklist:{jti}")
        return token_in_redis is not None
    except Exception:
        return False