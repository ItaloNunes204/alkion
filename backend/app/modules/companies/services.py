from app.core.extensions import db
from app.modules.companies.models import Company

def company_update_plans(old_plan_id: int, new_plan_id: int):
    Company.query.filter_by(plan_id=old_plan_id).update({"plan_id": new_plan_id})
    db.session.flush()
    db.session.commit()
