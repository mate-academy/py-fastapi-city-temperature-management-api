from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from city.models import DBCity
from database import Base


class DBTemperature(Base):
    __tablename__ = "Temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("City.id"))
    data_time = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
