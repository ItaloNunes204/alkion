from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

sync_bp = Blueprint("sync", __name__)

@sync_bp.get("/")
@jwt_required()
def index():
    return jsonify({"modulo": "sync", "status": "ok"}), 200