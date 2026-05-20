from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.exceptions import NotFoundError, ForbiddenError
from .models import Permission

permissions_ns = Namespace(
    "permissions",
    description="System permissions management"
)


@permissions_ns.route("/")
class PermissionList(Resource):

    @jwt_required()
    @permissions_ns.doc("list_permissions")
    def get(self):
        # TODO: verificar se usuario e system_admin, support ou dev
        permissions = Permission.query.filter_by(is_active=True).all()
        return [p.to_dict() for p in permissions], 200


@permissions_ns.route("/modules")
class PermissionsByModule(Resource):

    @jwt_required()
    @permissions_ns.doc("list_permissions_by_module")
    def get(self):
        permissions = Permission.query.filter_by(is_active=True).all()

        grouped = {}
        for p in permissions:
            if p.module not in grouped:
                grouped[p.module] = []
            grouped[p.module].append(p.to_dict())

        return grouped, 200