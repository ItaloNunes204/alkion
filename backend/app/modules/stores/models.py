from app.core.extensions import db
from datetime import datetime


class Store(db.Model):
    __tablename__ = "stores"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(200), nullable=False)
    code          = db.Column(db.String(20))
    phone         = db.Column(db.String(20))
    email         = db.Column(db.String(120))
    zip_code      = db.Column(db.String(10))
    street        = db.Column(db.String(255))
    street_number = db.Column(db.String(20))
    complement    = db.Column(db.String(100))
    neighborhood  = db.Column(db.String(100))
    city          = db.Column(db.String(100))
    state         = db.Column(db.String(2))
    is_active     = db.Column(db.Boolean, default=True)
    is_main       = db.Column(db.Boolean, default=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    company_id    = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    def to_dict(self):
        return {
            "id":           self.id,
            "name":         self.name,
            "code":         self.code,
            "phone":        self.phone,
            "email":        self.email,
            "zip_code":     self.zip_code,
            "street":       self.street,
            "street_number": self.street_number,
            "complement":   self.complement,
            "neighborhood": self.neighborhood,
            "city":         self.city,
            "state":        self.state,
            "is_active":    self.is_active,
            "is_main":      self.is_main,
            "company_id":   self.company_id,
            "created_at":   self.created_at.isoformat(),
            "modified_at":  self.modified_at.isoformat(),
        }