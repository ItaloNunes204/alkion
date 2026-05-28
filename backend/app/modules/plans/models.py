from app.core.extensions import db
from datetime import datetime

# Models for subscription plans
class Plan(db.Model):
    __tablename__ = "plans"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    description   = db.Column(db.Text)
    monthly_price = db.Column(db.Numeric(10, 2), nullable=False)
    annual_price  = db.Column(db.Numeric(10, 2), nullable=False)
    max_stores    = db.Column(db.Integer, nullable=False)
    max_users     = db.Column(db.Integer, nullable=False)
    is_active     = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id":            self.id,
            "name":          self.name,
            "description":   self.description,
            "monthly_price": float(self.monthly_price),
            "annual_price":  float(self.annual_price),
            "max_stores":    self.max_stores,
            "max_users":     self.max_users,
            "is_public": self.is_public,
            "created_at":    self.created_at,
            "modified_at":   self.modified_at,
        }