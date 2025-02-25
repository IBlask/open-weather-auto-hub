from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class AutomationRequest(db.Model):
    __tablename__ = 'automation_requests'
    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String(100), unique = False, nullable = False)
    automation_device_id = db.Column(UUID(as_uuid = True), db.ForeignKey('automation_devices.id'), nullable = False)
    port = db.Column(db.Integer, nullable = True, default = None)
    uri = db.Column(db.String(100), nullable = True, default = None)
    body = db.Column(db.String(255), nullable = True, default = None)
    