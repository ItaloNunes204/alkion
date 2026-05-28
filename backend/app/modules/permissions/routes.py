from flask import request

from app.core.security import requer_cliente
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.exceptions import NotFoundError, ForbiddenError
from app.core.responses import success_response, list_response
from .models import Permission
from app.core.extensions import db

permissions_ns = Namespace(
    "permissions",
    description="System permissions management"
)

def _get_current_user():
    from app.modules.users.models import User
    current_user = User.query.get(get_jwt_identity())
    if not current_user:
        raise NotFoundError("User not found")
    return current_user

# Helper functions for permission checks and data validation
def _check_admin_or_dev():
    from app.modules.users.models import User
    current_user = User.query.get(get_jwt_identity())
    if not current_user:
        raise ForbiddenError("User not found")
    allowed_roles = {"system_admin", "dev"}
    if current_user.role.name not in allowed_roles:
        raise ForbiddenError("Only system_admin and dev can manage plans")
    return current_user


@permissions_ns.route("/listAllPermissions")
class PermissionAllList(Resource):
    @jwt_required()
    @permissions_ns.doc("list_all_permissions")
    @requer_cliente("web")
    def get(self):
        _check_admin_or_dev()
        permissions = Permission.query.all()
        return list_response([p.to_dict() for p in permissions], "Permissions retrieved successfully")

@permissions_ns.route("/listPermissions")
class PermissionList(Resource):
    @jwt_required()
    @permissions_ns.doc("list_permissions")
    @requer_cliente("web")
    def get(self):
        current_user = _get_current_user()
        if not current_user.has_permission("users:manage_roles"):
            raise ForbiddenError("You don't have permission to view permissions")
        permissions = Permission.query.filter_by(is_active=True).all()
        return list_response([p.to_dict() for p in permissions], "Permissions retrieved successfully")

@permissions_ns.route("/updatePermissions/<int:permission_id>")
class PermissionUpdate(Resource):
    @jwt_required()
    @permissions_ns.doc("update_permission")
    @requer_cliente("web")
    def put(self, permission_id):
        _check_admin_or_dev()
        data = request.get_json() or {}
        updatable = ["is_active"]
        permission = Permission.query.get(permission_id)
        if not permission:
            raise NotFoundError("Permission not found")
        for field in updatable:
            if field in data:
                setattr(permission, field, data[field])
        db.session.commit()
        return success_response(permission.to_dict(), "Permission updated successfully")

@permissions_ns.route("/listPermissionsByModule")
class PermissionsByModule(Resource):
    @jwt_required()
    @permissions_ns.doc("list_permissions_by_module")
    @requer_cliente("web")
    def get(self):
        _check_admin_or_dev()
        permissions = Permission.query.all()
        grouped = {}
        for p in permissions:
            if p.module not in grouped:
                grouped[p.module] = []
            grouped[p.module].append(p.to_dict())

        return success_response(grouped, "Permissions retrieved successfully")
