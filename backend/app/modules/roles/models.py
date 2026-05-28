from app.core.extensions import db
from datetime import datetime

# Tabela intermediária role_permissions
role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id",       db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True),
)


class Role(db.Model):
    __tablename__ = "roles"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_system   = db.Column(db.Boolean, default=False)
    # True  = role nativo (system_admin, support, dev, owner)
    # False = role customizado pelo owner da empresa
    is_active   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    company_id  = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=True)
    # null       = role do sistema (system_admin, support, dev)
    # preenchido = role da empresa (owner + customizados)

    permissions = db.relationship(
        "Permission",
        secondary="role_permissions",
        backref="roles",
        lazy="joined"
    )

    def to_dict(self, include_permissions=False):
        data = {
            "id":          self.id,
            "name":        self.name,
            "description": self.description,
            "is_system":   self.is_system,
            "is_active":   self.is_active,
            "company_id":  self.company_id,
            "created_at":  self.created_at.isoformat(),
        }
        if include_permissions:
            data["permissions"] = [p.to_dict() for p in self.permissions]
        return data