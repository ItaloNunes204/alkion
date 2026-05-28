from app.core.security import requer_cliente
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.extensions import db
from app.core.exceptions import ValidationError, NotFoundError, ForbiddenError, ConflictError
from app.modules.permissions.models import Permission
from .models import Role
from app.core.responses import success_response, list_response, created_response
from app.modules.companies.models import Company
from app.modules.users.models import User

roles_ns = Namespace(
    "roles",
    description="Roles management"
)

role_model = roles_ns.model("RoleCreate", {
    "name":           fields.String(required=True,  description="Role name"),
    "description":    fields.String(required=False, description="Role description"),
    "permission_ids": fields.List(fields.Integer,   description="List of permission IDs"),
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



@roles_ns.route("/")
class RoleList(Resource):

    @jwt_required()
    @roles_ns.doc("list_roles")
    @requer_cliente("web")
    def get(self):
        current_user = _get_current_user()
        if not current_user.has_permission("users:manage_roles"):
            raise ForbiddenError("You don't have permission to view roles")
        roles = Role.query.filter(
            Role.is_active == True,
            db.or_(
                Role.company_id == current_user.company_id,
                Role.company_id.is_(None)
                )
        ).all()
        return list_response([r.to_dict(include_permissions=True) for r in roles], "Roles retrieved successfully")

    @jwt_required()
    @roles_ns.expect(role_model)
    @roles_ns.doc("create_role")
    @requer_cliente("web")
    def post(self):
        current_user = _get_current_user()
        if not current_user.has_permission("users:manage_roles"):
            raise ForbiddenError("You don't have permission to create roles")
        
        data = request.get_json() or {}
        if not data.get("name"):
            raise ValidationError("Field 'name' is required")

        system_names = ["system_admin", "support", "dev", "owner"]
        if data["name"].lower() in system_names:
            raise ConflictError(f"Cannot create a role with reserved name '{data['name']}'")

        role = Role(
            name        = data["name"].strip(),
            description = data.get("description", "").strip() or None,
            is_system   = False,
            company_id  = current_user.company_id,
        )

        db.session.add(role)
        db.session.flush()

        if data.get("permission_ids"):
            permissions = Permission.query.filter(
                Permission.id.in_(data["permission_ids"]),
                Permission.is_active == True
            ).all()
            role.permissions = permissions

        db.session.commit()
        return created_response(role.to_dict(include_permissions=True), "Role created successfully")

@roles_ns.route("/listAllRolesByCompany")
class RolesByCompany(Resource):
    @jwt_required()
    @roles_ns.doc("list_all_roles_by_company")
    @requer_cliente("web")
    def get(self):
        _check_admin_or_dev()
        companies = Company.query.filter_by(is_active=True).all()
        result = []
        for company in companies:
            roles = Role.query.filter_by(company_id=company.id).all()
            result.append({
                "company_id":   company.id,
                "company_name": company.trade_name,
                "roles": [r.to_dict(include_permissions=True) for r in roles]
                })
        return list_response(result, "Roles retrieved successfully")

@roles_ns.route("/<int:role_id>")
class RoleDetail(Resource):

    @jwt_required()
    @roles_ns.doc("get_role")
    @requer_cliente("web")
    def get(self, role_id):
        current_user = _get_current_user()
        if not current_user.has_permission("users:manage_roles"):
            raise ForbiddenError("You don't have permission to view roles")
        role = Role.query.get(role_id)
        if not role or not role.is_active:
            raise NotFoundError("Role not found")
        return success_response(role.to_dict(include_permissions=True), "Role retrieved successfully")

    @jwt_required()
    @roles_ns.doc("update_role")
    @requer_cliente("web")
    def put(self, role_id):
        current_user = _get_current_user()
        if not current_user.has_permission("users:manage_roles"):
            raise ForbiddenError("You don't have permission to update roles")
        role = Role.query.get(role_id)
        if not role or not role.is_active:
            raise NotFoundError("Role not found")

        if role.is_system:
            raise ForbiddenError("System roles cannot be modified")

        data = request.get_json() or {}

        if "name" in data and data["name"]:
            system_names = ["system_admin", "support", "dev", "owner"]
            if data["name"].lower() in system_names:
                raise ConflictError(f"Cannot use reserved name '{data['name']}'")
            role.name = data["name"].strip()

        if "description" in data:
            role.description = data["description"].strip() or None

        if "permission_ids" in data:
            permissions = Permission.query.filter(
                Permission.id.in_(data["permission_ids"]),
                Permission.is_active == True
            ).all()
            role.permissions = permissions

        db.session.commit()
        return success_response(role.to_dict(include_permissions=True), "Role updated successfully")

    @jwt_required()
    @roles_ns.doc("delete_role")
    @requer_cliente("web")
    def delete(self, role_id):
        current_user = _get_current_user()
        if not current_user.has_permission("users:manage_roles"):
            raise ForbiddenError("You don't have permission to delete roles")

        role = Role.query.get(role_id)
        if not role or not role.is_active:
            raise NotFoundError("Role not found")

        if role.is_system:
            raise ForbiddenError("System roles cannot be deleted")
        
        users_with_role = User.query.filter_by(role_id=role_id).count()
        if users_with_role > 0:
            raise ConflictError(
                f"Cannot delete role — {users_with_role} user(s) are assigned to it"
            )

        db.session.delete(role)
        db.session.commit()
        return success_response(None, "Role deleted successfully")