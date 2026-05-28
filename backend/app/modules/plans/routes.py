from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.exceptions import NotFoundError, ForbiddenError, ValidationError
from app.core.responses import success_response, list_response, message_response, created_response
from app.modules.companies.services import company_update_plans
from app.core.security import requer_cliente
from app.core.extensions import db
from .models import Plan

plans_ns = Namespace(
    "plans",
    description="Subscription plans management"
)

plan_model = plans_ns.model("PlanCreate", {
    "name":           fields.String(required=True,  description="Plan name"),
    "description":    fields.String(required=False, description="Plan description"),
    "monthly_price":  fields.Float(required=True,   description="Monthly price in BRL"),
    "annual_price":   fields.Float(required=True,   description="Annual price in BRL"),
    "max_stores":     fields.Integer(required=True,  description="Max stores (999 = unlimited)"),
    "max_users":      fields.Integer(required=True,  description="Max users per store (999 = unlimited)"),
    "is_public": fields.Boolean(required=False, description="Show as most popular"),
})

duplicate_model = plans_ns.model("PlanDuplicate", {
    "name":           fields.String(required=True,  description="Name for the new plan"),
    "monthly_price":  fields.Float(required=False,  description="Override monthly price"),
    "annual_price":   fields.Float(required=False,  description="Override annual price"),
    "max_stores":     fields.Integer(required=False, description="Override max stores"),
    "max_users":      fields.Integer(required=False, description="Override max users"),
    "description":    fields.String(required=False, description="Override description"),
    "is_public": fields.Boolean(required=False, description="Override public status"),
})


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


# Validates plan data for both creation and updates. For creation, all fields are required. For updates, only provided fields are validated.
def _validate_plan_data(data: dict, require_all: bool = True):
    if require_all:
        required = ["name", "monthly_price", "annual_price", "max_stores", "max_users"]
        for field in required:
            if data.get(field) is None:
                raise ValidationError(f"Field '{field}' is required")
    if "monthly_price" in data and data["monthly_price"] is not None:
        if data["monthly_price"] < 0:
            raise ValidationError("Monthly price must be non-negative")
    if "annual_price" in data and data["annual_price"] is not None:
        if data["annual_price"] < 0:
            raise ValidationError("Annual price must be non-negative")
    if "max_stores" in data and data["max_stores"] is not None:
        if data["max_stores"] < 0:
            raise ValidationError("Max stores must be non-negative")
    if "max_users" in data and data["max_users"] is not None:
        if data["max_users"] < 0:
            raise ValidationError("Max users must be non-negative")

# Route for listing all active plans 
@plans_ns.route("/")
class PlanList(Resource):
    @plans_ns.doc("list_plans")
    @requer_cliente("web")
    def get(self):
        plans = Plan.query.filter_by(is_active=True, is_public=True).all()
        return list_response([p.to_dict() for p in plans], "Plans retrieved successfully")

# Route for creating a new plan 
@plans_ns.route("/create")
class PlanCreate(Resource):
    @plans_ns.doc("create_plan", security="Bearer")
    @plans_ns.expect(plan_model)
    @requer_cliente("web")
    @jwt_required()
    def post(self):
        _check_admin_or_dev()
        data = request.get_json() or {}
        _validate_plan_data(data, require_all=True)
        plan = Plan(
            name           = data["name"].strip(),
            description    = data.get("description", "").strip() or None,
            monthly_price  = data["monthly_price"],
            annual_price   = data["annual_price"],
            max_stores     = data["max_stores"],
            max_users      = data["max_users"],
            is_public      = data.get("is_public", False),
            is_active      = True,
        )
        db.session.add(plan)
        db.session.commit()
        return created_response(plan.to_dict(), "Plan created successfully")

# Route for getting plan details by ID
@plans_ns.route("/byid/<int:plan_id>")
class PlanDetail(Resource):
    @plans_ns.doc("get_plan")
    @requer_cliente("web")
    def get(self, plan_id):
        plan = Plan.query.get(plan_id)
        if not plan:
            raise NotFoundError("Plan not found")
        return success_response(plan.to_dict(), "Plan retrieved successfully")

# Route for updating an existing plan by ID. Only provided fields will be updated.
@plans_ns.route("/update/<int:plan_id>")
class PlanUpdate(Resource):
    @plans_ns.doc("update_plan", security="Bearer")
    @plans_ns.expect(plan_model)
    @requer_cliente("web")
    @jwt_required()
    def put(self, plan_id):
        _check_admin_or_dev()
        plan = Plan.query.get(plan_id)
        if not plan:
            raise NotFoundError("Plan not found")
        data = request.get_json() or {}
        _validate_plan_data(data, require_all=False)
        if "name" in data and data["name"]:
            plan.name = data["name"].strip()
        if "description" in data:
            plan.description = data["description"].strip() or None
        if "monthly_price" in data and data["monthly_price"] is not None:
            plan.monthly_price = data["monthly_price"]
        if "annual_price" in data and data["annual_price"] is not None:
            plan.annual_price = data["annual_price"]
        if "max_stores" in data and data["max_stores"] is not None:
            plan.max_stores = data["max_stores"]
        if "max_users" in data and data["max_users"] is not None:
            plan.max_users = data["max_users"]
        if "is_public" in data:
            plan.is_public = data["is_public"]
        db.session.commit()
        return success_response(plan.to_dict(), "Plan updated successfully")

# Route for activating/deactivating a plan by ID. This is a soft delete that toggles the active status.
@plans_ns.route("/toggle-status/<int:plan_id>")
class TogglePlanStatus(Resource):
    @plans_ns.doc("toggle_plan_status", security="Bearer")
    @requer_cliente("web")
    @jwt_required()
    def post(self, plan_id):
        _check_admin_or_dev()
        plan = Plan.query.get(plan_id)
        if not plan:
            raise NotFoundError("Plan not found")
        if plan.is_active:
            plan.is_active = False
        else:
            plan.is_active = True
        db.session.commit()
        return message_response(f"Plan '{plan.name}' toggle status successfully"), 200

# Route for permanently deleting a plan by ID. This requires specifying another plan to replace any users subscribed to the deleted plan.
@plans_ns.route("/delete/<int:plan_id_delete>/<int:plan_id_replace>")
class PlanDelete(Resource):
    @plans_ns.doc("delete_plan", security="Bearer")
    @requer_cliente("web")
    @jwt_required()
    def delete(self, plan_id_delete, plan_id_replace):
        _check_admin_or_dev()
        plan_to_delete = Plan.query.get(plan_id_delete)
        plan_to_replace = Plan.query.get(plan_id_replace)
        if not plan_to_delete:
            raise NotFoundError("Plan to delete not found")
        if not plan_to_replace:
            raise NotFoundError("Plan to replace not found")
        company_update_plans(plan_to_delete.id, plan_to_replace.id)
        db.session.delete(plan_to_delete)
        db.session.commit()
        return message_response(f"Plan '{plan_to_delete.name}' permanently deleted"), 200

# Route for duplicating an existing plan by ID. The new plan will have the same attributes as the original, but with a modified name and optional overrides.
@plans_ns.route("/duplicate/<int:plan_id>")
class PlanDuplicate(Resource):
    @plans_ns.doc("duplicate_plan", security="Bearer")
    @plans_ns.expect(duplicate_model)
    @requer_cliente("web")
    @jwt_required()
    def post(self, plan_id):
        _check_admin_or_dev()
        original = Plan.query.get(plan_id)
        if not original:
            raise NotFoundError("Plan not found")
        data = request.get_json() or {}
        if not data.get("name"):
            raise ValidationError("Field 'name' is required")
        new_plan = Plan(
            name           = (data["name"] + " (Copy)").strip(),
            description = (data.get("description") or original.description or "").strip() or None,
            monthly_price  = data.get("monthly_price", original.monthly_price),
            annual_price   = data.get("annual_price", original.annual_price),
            max_stores     = data.get("max_stores", original.max_stores),
            max_users      = data.get("max_users", original.max_users),
            is_public      = data.get("is_public", original.is_public),
            is_active      = True,
        )
        db.session.add(new_plan)
        db.session.commit()
        return created_response(new_plan.to_dict(), "Plan duplicated successfully")
