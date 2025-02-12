from app import db
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid


class AutomationDevice(db.Model):
    __tablename__ = 'automation_devices'
    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String(100), unique = False, nullable = False)
    ip_address = db.Column(db.String, unique = True, nullable = False)