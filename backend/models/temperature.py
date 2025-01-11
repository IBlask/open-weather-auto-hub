from app import db
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid


class Temperature(db.Model):
    __tablename__ = 'temperatures'
    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    value = db.Column(db.Float, unique = False, nullable = False)
    measuring_device_id = db.Column(UUID(as_uuid = True), db.ForeignKey('measuring_devices.id'), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)

    def to_dict(self):
        return {
            'value': self.value,
            'measuring_device_id': str(self.measuring_device_id),
            'measured_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }