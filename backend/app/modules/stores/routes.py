from app.core.security import requer_cliente
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.extensions import db
from app.core.exceptions import ConflictError, ValidationError, NotFoundError, ForbiddenError
from app.core.responses import success_response, list_response, created_response
from .models import Store
from app.modules.companies.models import Company
from app.modules.users.models import User

stores_ns = Namespace(
    "stores",
    description="Store management"
)

store_model = stores_ns.model("StoreCreate", {
    "name":         fields.String(required=True,  description="Store name"),
    "code":         fields.String(required=False, description="Store code"),
    "phone":        fields.String(required=False, description="Phone"),
    "email":        fields.String(required=False, description="Email"),
    "zip_code":     fields.String(required=False, description="ZIP code"),
    "street":       fields.String(required=False, description="Street"),
    "street_number": fields.String(required=False, description="Street number"),
    "complement":   fields.String(required=False, description="Complement"),
    "neighborhood": fields.String(required=False, description="Neighborhood"),
    "city":         fields.String(required=False, description="City"),
    "state":        fields.String(required=False, description="State"),
    "is_main":      fields.Boolean(required=False, description="Is main store"),
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

@stores_ns.route("/listAllStores")
class StoreAllList(Resource):
    @jwt_required()
    @stores_ns.doc("list_all_stores")
    @requer_cliente("web")
    def get(self):
        _check_admin_or_dev()
        companies = Company.query.filter_by(is_active=True).all()
        result = []
        for company in companies:
            stores = Store.query.filter_by(company_id=company.id).all()
            result.append({
                "company_id":   company.id,
                "company_name": company.trade_name,
                "stores":       [s.to_dict() for s in stores]
            })
        return list_response(result, "Companies with stores retrieved successfully")

@stores_ns.route("/")
class StoreList(Resource):

    @jwt_required()
    @stores_ns.doc("list_stores")
    @requer_cliente("web")
    def get(self):
        current_user = _get_current_user()
        if not current_user.has_permission("stores:view"):
            raise ForbiddenError("You don't have permission to view stores")
        stores = Store.query.filter_by(is_active=True, company_id=current_user.company_id).all()
        return list_response([s.to_dict() for s in stores], "Stores retrieved successfully")

    @jwt_required()
    @stores_ns.expect(store_model)
    @stores_ns.doc("create_store")
    @requer_cliente("web")
    def post(self):
        current_user = _get_current_user()
        if not current_user.has_permission("stores:create"):
            raise ForbiddenError("You don't have permission to create stores")
        data = request.get_json() or {}

        if not data.get("name"):
            raise ValidationError("Field 'name' is required")


        if data.get("is_main"):
            Store.query.filter_by(
                is_main=True,
                company_id=current_user.company_id
            ).update({"is_main": False})

        store = Store(
            name          = data["name"].strip(),
            code          = data.get("code", "").strip() or None,
            phone         = data.get("phone", "").strip() or None,
            email         = data.get("email", "").strip().lower() or None,
            zip_code      = data.get("zip_code", "").strip() or None,
            street        = data.get("street", "").strip() or None,
            street_number = data.get("street_number", "").strip() or None,
            complement    = data.get("complement", "").strip() or None,
            neighborhood  = data.get("neighborhood", "").strip() or None,
            city          = data.get("city", "").strip() or None,
            state         = data.get("state", "").strip().upper() or None,
            is_main       = data.get("is_main", False),
            company_id    = current_user.company_id,  
        )

        db.session.add(store)
        db.session.commit()
        return created_response(store.to_dict(), "Store created successfully")


@stores_ns.route("/<int:store_id>")
class StoreDetail(Resource):

    @jwt_required()
    @stores_ns.doc("get_store")
    @requer_cliente("web")
    def get(self, store_id):
        current_user = _get_current_user()
        if not current_user.has_permission("stores:view"):
            raise ForbiddenError("You don't have permission to view stores")

        store = Store.query.get(store_id)
        if not store or not store.is_active:
            raise NotFoundError("Store not found")
        
        if store.company_id != current_user.company_id:
            raise ForbiddenError("Access denied")

        return success_response(store.to_dict(), "Store retrieved successfully")

    @jwt_required()
    @stores_ns.doc("update_store")
    @requer_cliente("web")
    def put(self, store_id):

        current_user = _get_current_user()
        if not current_user.has_permission("stores:edit"):
            raise ForbiddenError("You don't have permission to edit stores")

        store = Store.query.get(store_id)
        if not store or not store.is_active:
            raise NotFoundError("Store not found")
        
        if store.company_id != current_user.company_id:
            raise ForbiddenError("Access denied")

        data = request.get_json() or {}

        updatable = [
            "name", "code", "phone", "email", "zip_code",
            "street", "street_number", "complement",
            "neighborhood", "city", "state"
        ]
        for field in updatable:
            if field in data and data[field] is not None:
                setattr(store, field, data[field].strip())

        if "is_main" in data and data["is_main"]:
            Store.query.filter_by(is_main=True, company_id=current_user.company_id).update({"is_main": False})
            store.is_main = True

        db.session.commit()
        return success_response(store.to_dict(), "Store updated successfully")

    @jwt_required()
    @stores_ns.doc("delete_store")
    @requer_cliente("web")
    def delete(self, store_id):
        current_user = _get_current_user()
        if not current_user.has_permission("stores:delete"):
            raise ForbiddenError("You don't have permission to delete stores")
        
        store = Store.query.get(store_id)
        if not store or not store.is_active:
            raise NotFoundError("Store not found")
        
        if store.company_id != current_user.company_id:
            raise ForbiddenError("Access denied")

        if store.is_main:
            raise ForbiddenError("Cannot delete the main store")
        users_in_store = User.query.filter_by(store_id=store_id).count()
        if users_in_store > 0:
            raise ConflictError(f"Cannot delete store — {users_in_store} user(s) are assigned to it")

        db.session.delete(store)
        db.session.commit()
        return success_response(None, "Store deleted successfully")
