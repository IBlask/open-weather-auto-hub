from app import db


class Email(db.Model):
    __tablename__ = 'emails'
    email = db.Column(db.String(100), primary_key = True)
    is_enabled = db.Column(db.Boolean, nullable = False, default = True)
    