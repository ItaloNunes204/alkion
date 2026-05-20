import re
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from app.core.extensions import db
from app.core.exceptions import ValidationError, ConflictError, ForbiddenError, NotFoundError
from app.utils.validators import validate_cnpj, validate_password
from .models import Company

companies_ns = Namespace(
    "companies",
    description="Company registration and management"
)

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

        if not validate_cnpj(data["tax_id"]):
            raise ValidationError("Invalid CNPJ")

        is_valid, message = validate_password(data["password"])
        if not is_valid:
            raise ValidationError(message)

        if Company.query.filter_by(tax_id=re.sub(r'[^0-9]', '', data["tax_id"])).first():
            raise ConflictError("A company with this tax ID already exists")

        if Company.query.filter_by(email=data["email"].strip().lower()).first():
            raise ConflictError("A company with this email already exists")

        company = Company(
            legal_name    = data["legal_name"].strip(),
            trade_name    = data["trade_name"].strip(),
            tax_id        = re.sub(r'[^0-9]', '', data["tax_id"]),
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

        # TODO: Create owner user when users table is implemented
        # user = User(
        #     name       = data["responsible"],
        #     email      = data["email"],
        #     role       = "owner",
        #     company_id = company.id,
        # )
        # user.set_password(data["password"])
        # db.session.add(user)

        db.session.commit()

        access_token  = create_access_token(identity=str(company.id))
        refresh_token = create_refresh_token(identity=str(company.id))

        return {
            "message":       "Company registered successfully",
            "access_token":  access_token,
            "refresh_token": refresh_token,
            "company":       company.to_dict(),
        }, 201


@companies_ns.route("/")
class CompanyList(Resource):

    @jwt_required()
    @companies_ns.doc("list_companies", security="Bearer")
    def get(self):
        # TODO: when users table is ready, check if user is system admin
        # current_id = get_jwt_identity()
        # user = User.query.get(current_id)
        # if not user or user.role != "system_admin":
        #     raise ForbiddenError("Only system admins can list all companies")

        companies = Company.query.filter_by(is_active=True).all()
        return [c.to_dict() for c in companies], 200


@companies_ns.route("/<int:company_id>")
class CompanyDetail(Resource):

    @jwt_required()
    @companies_ns.doc("get_company", security="Bearer")
    def get(self, company_id):
        company = Company.query.get(company_id)
        if not company:
            raise NotFoundError("Company not found")

        # TODO: when users table is ready, verify user belongs to company
        # current_id = get_jwt_identity()
        # user = User.query.get(current_id)
        # if not user or user.company_id != company_id:
        #     raise ForbiddenError("Access denied")

        return company.to_dict(), 200

    @jwt_required()
    @companies_ns.doc("update_company", security="Bearer")
    def put(self, company_id):
        company = Company.query.get(company_id)
        if not company:
            raise NotFoundError("Company not found")

        # TODO: when users table is ready, verify user is owner
        # current_id = get_jwt_identity()
        # user = User.query.get(current_id)
        # if not user or user.company_id != company_id or user.role != "owner":
        #     raise ForbiddenError("Only the company owner can update company information")

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
        return company.to_dict(), 200