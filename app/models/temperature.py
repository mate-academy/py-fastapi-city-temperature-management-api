# models/temperature.py
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from app.db import Base
from datetime import datetime

class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
