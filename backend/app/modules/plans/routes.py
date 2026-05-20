from flask import jsonify
from flask_restx import Namespace, Resource
from app.core.extensions import db
from .models import Plan

plans_ns = Namespace(
    "plans",
    description="Subscription plans management"
)


@plans_ns.route("/")
class PlanList(Resource):
    @plans_ns.doc("list_plans")
    def get(self):
        """Returns all active plans"""
        plans = Plan.query.filter_by(is_active=True).all()
        return [p.to_dict() for p in plans], 200


@plans_ns.route("/<int:plan_id>")
class PlanDetail(Resource):
    @plans_ns.doc("get_plan")
    def get(self, plan_id):
        plan = Plan.query.get(plan_id)
        if not plan:
            return {"erro": "Plan not found"}, 404
        return plan.to_dict(), 200