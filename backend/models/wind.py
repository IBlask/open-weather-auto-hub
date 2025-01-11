from app import db
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid


class Wind(db.Model):
    __tablename__ = 'winds'
    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    speed = db.Column(db.Float, unique = False, nullable = False)
    direction = db.Column(db.Float, unique = False, nullable = False)
    measuring_device_id = db.Column(UUID(as_uuid = True), db.ForeignKey('measuring_devices.id'), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)

    def to_dict(self):
        return {
            'speed': self.speed,
            'direction': self.direction,
            'measuring_device_id': str(self.measuring_device_id),
            'measured_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }