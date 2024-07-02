import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime, Float

from app.models import Base


class TemperatureModel(Base):
    __tablename__ = "temperatures"
    id = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    city_id = Column(String, ForeignKey('cities.id'), nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float, nullable=False)
