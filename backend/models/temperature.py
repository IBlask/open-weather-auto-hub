from app import db
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid


class Temperature(db.Model):
    __tablename__ = 'temperatures'
    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    value = db.Column(db.Float, unique = False, nullable = False)
    measuring_device_id = db.Column(UUID(as_uuid = True), db.ForeignKey('measuring_devices.id'), nullable = False)
    measuring_device = db.relationship('MeasuringDevice', back_populates = 'temperatures')
    created_at = db.Column(db.DateTime, nullable = False)