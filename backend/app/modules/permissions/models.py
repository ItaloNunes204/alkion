from app.core.extensions import db


class Permission(db.Model):
    __tablename__ = "permissions"

    id          = db.Column(db.Integer, primary_key=True)
    code        = db.Column(db.String(100), unique=True, nullable=False)
    module      = db.Column(db.String(50), nullable=False)
    action      = db.Column(db.String(30), nullable=False)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active   = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id":          self.id,
            "code":        self.code,
            "module":      self.module,
            "action":      self.action,
            "name":        self.name,
            "description": self.description,
            "is_active":   self.is_active,
        }