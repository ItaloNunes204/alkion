from app.core.extensions import db
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = "users"
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone         = db.Column(db.String(20))
    avatar_url    = db.Column(db.String(500))
    is_active     = db.Column(db.Boolean, default=True)
    last_access   = db.Column(db.DateTime, nullable=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    company_id    = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    store_id      = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=True)
    role_id       = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    role    = db.relationship("Role", backref="users", lazy="joined")
    store   = db.relationship("Store", backref="users", lazy="joined")
    company = db.relationship("Company", backref="users", lazy="joined")

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password_hash.encode("utf-8")
        )

    def update_last_access(self):
        self.last_access = datetime.utcnow()
        db.session.commit()

    def has_permission(self, code: str) -> bool:
        if not self.role:
            return False
        if self.role.name in ("system_admin", "owner"):
            return True
        return any(p.code == code for p in self.role.permissions)

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "email":       self.email,
            "phone":       self.phone,
            "avatar_url":  self.avatar_url,
            "is_active":   self.is_active,
            "last_access": self.last_access.isoformat() if self.last_access else None,
            "created_at":  self.created_at.isoformat(),
            "company_id":  self.company_id,
            "store_id":    self.store_id,
            "role":        self.role.name if self.role else None,
            "role_id":     self.role_id,
        }
