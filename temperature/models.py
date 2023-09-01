from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base


class CityTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="temperature")
