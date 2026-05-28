from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from app.core.extensions import db, redis_client
from app.core.exceptions import ValidationError, NotFoundError, ForbiddenError
from app.core.responses import success_response, message_response
from app.core.security import requer_cliente
from app.modules.users.models import User

auth_ns = Namespace(
    "auth",
    description="Authentication"
)

login_model = auth_ns.model("Login", {
    "email":    fields.String(required=True, description="Email"),
    "password": fields.String(required=True, description="Password"),
})

@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.doc("login")
    @auth_ns.expect(login_model)
    @requer_cliente("web", "mobile", "desktop")
    def post(self):
        data = request.get_json() or {}

        if not data.get("email") or not data.get("password"):
            raise ValidationError("Email and password are required")

        user = User.query.filter_by(
            email=data["email"].strip().lower()
        ).first()

        if not user or not user.check_password(data["password"]):
            raise ForbiddenError("Invalid email or password")

        if not user.is_active:
            raise ForbiddenError("User account is deactivated")

        user.update_last_access()

        access_token  = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return success_response({
            "access_token":  access_token,
            "refresh_token": refresh_token,
            "user":          user.to_dict(),
        }, "Login successful")


@auth_ns.route("/refresh")
class Refresh(Resource):

    @jwt_required(refresh=True)
    @auth_ns.doc("refresh_token", security="Bearer")
    @requer_cliente("web", "mobile", "desktop")
    def post(self):
        current_id = get_jwt_identity()
        user = User.query.get(current_id)

        if not user or not user.is_active:
            raise ForbiddenError("User not found or deactivated")

        access_token = create_access_token(identity=str(user.id))

        return success_response(
            {"access_token": access_token},
            "Token refreshed successfully"
        )


@auth_ns.route("/me")
class Me(Resource):

    @jwt_required()
    @auth_ns.doc("get_current_user", security="Bearer")
    @requer_cliente("web", "mobile", "desktop")
    def get(self):
        current_id = get_jwt_identity()
        user = User.query.get(current_id)

        if not user or not user.is_active:
            raise NotFoundError("User not found")

        return success_response(user.to_dict(), "User retrieved successfully")


@auth_ns.route("/logout")
class Logout(Resource):

    @jwt_required()
    @auth_ns.doc("logout", security="Bearer")
    @requer_cliente("web", "mobile", "desktop")
    def post(self):
        jti = get_jwt()["jti"]
        try:
            redis_client.set(f"blocklist:{jti}", "1", ex=3600)
        except Exception:
            pass
        return message_response("Logged out successfully")
