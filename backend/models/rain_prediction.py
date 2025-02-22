from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class RainPrediction(db.Model):
    __tablename__ = 'rain_prediction'
    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    prediction = db.Column(db.Float, unique = False, nullable = False)
    created_at = db.Column(db.DateTime, unique = False, nullable = False)