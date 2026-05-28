from app.core.security import requer_cliente
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
import re
from app.core.extensions import db
from app.core.responses import success_response, list_response, message_response, created_response
from app.core.exceptions import ValidationError, ConflictError, NotFoundError, ForbiddenError
from app.utils.validators import validate_cnpj, validate_password
from app.modules.roles.models import Role
from app.modules.stores.models import Store
from .models import Company

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

def _get_company():
    from app.modules.users.models import User
    current_user = User.query.get(get_jwt_identity())
    if not current_user:
        raise NotFoundError("User not found")
    company = Company.query.get(current_user.company_id)
    if not company:
        raise NotFoundError("Company not found")
    return current_user, company

# API Namespace
companies_ns = Namespace(
    "companies",
    description="Company registration and management"
)

# Swagger model for company registration
register_model = companies_ns.model("CompanyRegister", {
    "legal_name":    fields.String(required=True,  description="Legal company name"),
    "trade_name":    fields.String(required=True,  description="Trade name"),
    "tax_id":        fields.String(required=True,  description="CNPJ"),
    "site":          fields.String(required=True,  description="Website"),
    "email":         fields.String(required=True,  description="Email"),
    "phone":         fields.String(required=True,  description="Phone"),
    "responsible":   fields.String(required=True,  description="Responsible person"),
    "password":      fields.String(required=True,  description="Password"),
    "zip_code":      fields.String(required=True,  description="ZIP code"),
    "street":        fields.String(required=True,  description="Street"),
    "street_number": fields.String(required=True,  description="Street number"),
    "complement":    fields.String(required=False, description="Complement"),
    "neighborhood":  fields.String(required=True,  description="Neighborhood"),
    "city":          fields.String(required=True,  description="City"),
    "state":         fields.String(required=True,  description="State"),
    "plan_id":       fields.Integer(required=False, description="Plan ID"),
    "billing_cycle": fields.String(required=False, description="monthly or annual"),
})

@companies_ns.route("/register")
class CompanyRegister(Resource):
    @companies_ns.expect(register_model)
    @companies_ns.doc("register_company")
    @requer_cliente("web")
    def post(self):
        data = request.get_json() or {}
        required = [
            "legal_name", "trade_name", "tax_id", "site",
            "email", "phone", "responsible", "password",
            "zip_code", "street", "street_number",
            "neighborhood", "city", "state"
        ]
        for field in required:
            if not data.get(field, "").strip():
                raise ValidationError(f"Field '{field}' is required")
            
        clean_tax_id = re.sub(r'[^0-9]', '', data["tax_id"])

        if not validate_cnpj(data["tax_id"]):
            raise ValidationError("Invalid CNPJ")

        is_valid, message = validate_password(data["password"])
        if not is_valid:
            raise ValidationError(message)
        
        if Company.query.filter_by(tax_id=clean_tax_id).first():
            raise ConflictError("A company with this tax ID already exists")

        if Company.query.filter_by(email=data["email"].strip().lower()).first():
            raise ConflictError("A company with this email already exists")

        owner_role = Role.query.filter_by(name="owner").first()
        if not owner_role:
            raise ValidationError("System not properly configured — owner role not found")
        company = Company(
            legal_name    = data["legal_name"].strip(),
            trade_name    = data["trade_name"].strip(),
            tax_id        = clean_tax_id,
            site          = data["site"].strip(),
            email         = data["email"].strip().lower(),
            phone         = data["phone"].strip(),
            responsible   = data["responsible"].strip(),
            zip_code      = data["zip_code"].strip(),
            street        = data["street"].strip(),
            street_number = data["street_number"].strip(),
            complement    = data.get("complement", "").strip() or None,
            neighborhood  = data["neighborhood"].strip(),
            city          = data["city"].strip(),
            state         = data["state"].strip().upper(),
            plan_id       = data.get("plan_id"),
            status        = "trial",
        )

        db.session.add(company)
        db.session.flush()

        main_store = Store(
            name          = data["trade_name"].strip(),
            street        = data["street"].strip(),
            street_number = data["street_number"].strip(),
            complement    = data.get("complement", "").strip() or None,
            neighborhood  = data["neighborhood"].strip(),
            city          = data["city"].strip(),
            state         = data["state"].strip().upper(),
            zip_code      = data["zip_code"].strip(),
            phone         = data["phone"].strip(),
            is_main       = True,
            company_id    = company.id,
        )

        db.session.add(main_store)
        db.session.flush()

        from app.modules.users.models import User
        owner = User(
            name       = data["responsible"].strip(),
            email      = data["email"].strip().lower(),
            phone      = data["phone"].strip(),
            role_id    = owner_role.id,
            store_id   = main_store.id,
            company_id = company.id,
        )
        owner.set_password(data["password"])

        db.session.add(owner)
        db.session.commit()

        access_token  = create_access_token(identity=str(owner.id))
        refresh_token = create_refresh_token(identity=str(owner.id))

        return created_response({
            "access_token":  access_token,
            "refresh_token": refresh_token,
            "user":          owner.to_dict(),
            "company":       company.to_dict()
            }, "Company registered successfully")


@companies_ns.route("/companiesList")
class CompanyList(Resource):
    @jwt_required()
    @companies_ns.doc("list_companies", security="Bearer")
    @requer_cliente("web")
    def get(self):
        _check_admin_or_dev()
        companies = Company.query.filter_by(is_active=True).all()
        return list_response([c.to_dict() for c in companies], "Companies retrieved successfully")


@companies_ns.route("/companiesInformation")
class CompanyDetail(Resource):
    @jwt_required()
    @companies_ns.doc("get_company", security="Bearer")
    @requer_cliente("web")
    def get(self):
        current_user, company = _get_company()
        if not current_user.has_permission("company:view"):
            raise ForbiddenError("You don't have permission to view company information")
        return success_response(company.to_dict(), "Company information retrieved successfully")

    @jwt_required()
    @companies_ns.doc("update_company", security="Bearer")
    @requer_cliente("web")
    def put(self):
        current_user, company = _get_company()
        if not current_user.has_permission("company:edit"):
            raise ForbiddenError("You don't have permission to update company information")
        data = request.get_json() or {}
        updatable = [
            "legal_name", "trade_name", "site", "phone",
            "responsible", "zip_code", "street", "street_number",
            "complement", "neighborhood", "city", "state"
        ]
        for field in updatable:
            if field in data and data[field]:
                setattr(company, field, data[field].strip())

        db.session.commit()
        return success_response(company.to_dict(), "Company information updated successfully")