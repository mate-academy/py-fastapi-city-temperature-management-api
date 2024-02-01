from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from city.models import DBCity
from database import Base
from datetime import datetime


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, default=datetime.now)
    temperature = Column(Float)

    city = relationship(DBCity, back_populates="temperatures")
