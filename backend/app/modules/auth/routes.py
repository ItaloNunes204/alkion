from flask import Blueprint, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/")
def index():
    return jsonify({"modulo": "auth", "status": "ok"}), 200