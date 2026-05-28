from app.core.security import requer_cliente
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.extensions import db
from app.core.exceptions import ValidationError, ConflictError, NotFoundError, ForbiddenError
from app.core.responses import success_response, list_response, created_response
from app.utils.validators import validate_password
from app.modules.roles.models import Role
from app.modules.companies.models import Company
from .models import User

users_ns = Namespace(
    "users",
    description="User management"
)

user_model = users_ns.model("UserCreate", {
    "name":     fields.String(required=True,  description="Full name"),
    "email":    fields.String(required=True,  description="Email"),
    "password": fields.String(required=True,  description="Password"),
    "phone":    fields.String(required=False, description="Phone"),
    "role_id":  fields.Integer(required=True, description="Role ID"),
    "store_id": fields.Integer(required=False, description="Store ID"),
})


def _get_current_user():
    current_user = User.query.get(get_jwt_identity())
    if not current_user:
        raise NotFoundError("User not found")
    return current_user

# Helper functions for permission checks and data validation
def _check_admin_or_dev():
    current_user = User.query.get(get_jwt_identity())
    if not current_user:
        raise ForbiddenError("User not found")
    allowed_roles = {"system_admin", "dev"}
    if current_user.role.name not in allowed_roles:
        raise ForbiddenError("Only system_admin and dev can manage plans")
    return current_user

@users_ns.route("/")
class UserList(Resource):

    @jwt_required()
    @users_ns.doc("list_users")
    @requer_cliente("web")
    def get(self):
        current_user = _get_current_user()

        if not current_user.has_permission("users:view"):
            raise ForbiddenError("You don't have permission to view users")

        users = User.query.filter_by(
            company_id=current_user.company_id
        ).all()

        return list_response([u.to_dict() for u in users], "Users retrieved successfully")

    @jwt_required()
    @users_ns.expect(user_model)
    @users_ns.doc("create_user")
    @requer_cliente("web")
    def post(self):
        current_user = _get_current_user()

        if not current_user.has_permission("users:create"):
            raise ForbiddenError("You don't have permission to create users")

        data = request.get_json() or {}

        required = ["name", "email", "password", "role_id"]
        for field in required:
            if not data.get(field):
                raise ValidationError(f"Field '{field}' is required")

        is_valid, message = validate_password(data["password"])
        if not is_valid:
            raise ValidationError(message)

        if User.query.filter_by(email=data["email"].strip().lower()).first():
            raise ConflictError("A user with this email already exists")

        role = Role.query.filter(
            Role.id == data["role_id"],
            db.or_(
                Role.company_id == current_user.company_id,
                Role.company_id.is_(None)  # permite roles do sistema (owner, etc)
            )
        ).first()
        if not role:
            raise NotFoundError("Role not found")

        if role.name == "system_admin":
            raise ForbiddenError("Cannot assign system_admin role")

        user = User(
            name       = data["name"].strip(),
            email      = data["email"].strip().lower(),
            phone      = data.get("phone"),
            role_id    = data["role_id"],
            store_id   = data.get("store_id"),
            company_id = current_user.company_id,
        )
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return created_response(user.to_dict(), "User created successfully")

@users_ns.route("/me")
class UserMe(Resource):
    @jwt_required()
    @users_ns.doc("get_current_user")
    @requer_cliente("web")
    def get(self):
        current_user = _get_current_user()
        return success_response(current_user.to_dict(), "Current user retrieved successfully")

@users_ns.route("/listallUsers")
class UserListAll(Resource):
    @jwt_required()
    @users_ns.doc("list_all_users")
    @requer_cliente("web")
    def get(self):
        _check_admin_or_dev()
        companies = Company.query.filter_by(is_active=True).all()
        result = []
        for company in companies:
            users = User.query.filter_by(company_id=company.id).all()
            data = company.to_dict()
            data["users"] = [u.to_dict() for u in users]
            result.append(data)
        return list_response(result, "All users retrieved successfully")

@users_ns.route("/<int:user_id>")
class UserDetail(Resource):

    @jwt_required()
    @users_ns.doc("get_user")
    @requer_cliente("web")
    def get(self, user_id):
        current_user = _get_current_user()

        user = User.query.get(user_id)
        if not user or user.company_id != current_user.company_id:
            raise NotFoundError("User not found")

        if not current_user.has_permission("users:view") and str(current_user.id) != str(user_id):
            raise ForbiddenError("Access denied")
        
        return success_response(user.to_dict(), "User retrieved successfully")

    @jwt_required()
    @users_ns.doc("update_user")
    @requer_cliente("web")
    def put(self, user_id):
        current_user = _get_current_user()

        user = User.query.get(user_id)
        if not user or user.company_id != current_user.company_id:
            raise NotFoundError("User not found")

        if not current_user.has_permission("users:edit") and str(current_user.id) != str(user_id):
            raise ForbiddenError("You don't have permission to edit this user")

        data = request.get_json() or {}

        updatable = ["name", "phone", "avatar_url"]
        for field in updatable:
            if field in data and data[field]:
                setattr(user, field, data[field].strip())

        if "role_id" in data and current_user.has_permission("users:manage_roles"):
            role = Role.query.filter(
                Role.id == data["role_id"],
                db.or_(
                    Role.company_id == current_user.company_id,
                    Role.company_id.is_(None)
                )
            ).first()
            if not role:
                raise NotFoundError("Role not found")
            if role.name == "system_admin":
                raise ForbiddenError("Cannot assign system_admin role")
            user.role_id = data["role_id"]

        db.session.commit()
        return success_response(user.to_dict(), "User updated successfully")

    @jwt_required()
    @users_ns.doc("delete_user")
    @requer_cliente("web")
    def delete(self, user_id):

        current_user = _get_current_user()

        if not current_user.has_permission("users:delete"):
            raise ForbiddenError("You don't have permission to delete users")

        user = User.query.get(user_id)
        if not user or user.company_id != current_user.company_id:
            raise NotFoundError("User not found")

        if user.role and user.role.name == "owner":
            raise ForbiddenError("Cannot deactivate the company owner")

        db.session.delete(user)
        db.session.commit()
        return success_response(None, "User deleted successfully")
