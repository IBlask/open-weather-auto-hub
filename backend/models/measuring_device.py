from app import db
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid


def generate_public_key():
    return str(uuid.uuid4());


class MeasuringDevice(db.Model):
    __tablename__ = 'measuring_devices'
    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String(100), unique = False, nullable = False)
    public_key = db.Column(db.String, unique = True, nullable = False, default = generate_public_key)