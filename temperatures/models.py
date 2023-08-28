from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from database import Base
from cities.models import CityDB


class TemperatureDB(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, server_default=func.now())
    temperature = Column(Float)

    city = relationship(CityDB, back_populates="temperatures")
