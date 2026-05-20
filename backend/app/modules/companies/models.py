from app.core.extensions import db
from datetime import datetime


class Company(db.Model):
    __tablename__ = "companies"

    id            = db.Column(db.Integer, primary_key=True)
    legal_name    = db.Column(db.String(200), nullable=False)
    trade_name    = db.Column(db.String(200), nullable=False)
    tax_id        = db.Column(db.String(18), unique=True, nullable=False)
    site          = db.Column(db.String(255), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    phone         = db.Column(db.String(20), nullable=False)
    responsible   = db.Column(db.String(120), nullable=False)
    is_active     = db.Column(db.Boolean, default=True)
    status        = db.Column(db.String(20), default="trial")
    zip_code      = db.Column(db.String(10), nullable=False)
    street        = db.Column(db.String(255), nullable=False)
    street_number = db.Column(db.String(20), nullable=False)
    complement    = db.Column(db.String(100))
    neighborhood  = db.Column(db.String(100), nullable=False)
    city          = db.Column(db.String(100), nullable=False)
    state         = db.Column(db.String(2), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    plan_id       = db.Column(db.Integer, db.ForeignKey("plans.id"), nullable=True)

    plan = db.relationship("Plan", backref="companies")

    def to_dict(self):
        return {
            "id":           self.id,
            "legal_name":   self.legal_name,
            "trade_name":   self.trade_name,
            "tax_id":       self.tax_id,
            "site":         self.site,
            "email":        self.email,
            "phone":        self.phone,
            "responsible":  self.responsible,
            "status":       self.status,
            "zip_code":     self.zip_code,
            "street":       self.street,
            "street_number": self.street_number,
            "complement":   self.complement,
            "neighborhood": self.neighborhood,
            "city":         self.city,
            "state":        self.state,
            "plan_id":      self.plan_id,
            "created_at":   self.created_at.isoformat(),
            "modified_at":  self.modified_at.isoformat(),
        }