from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from city.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=True)
    temperature = Column(Float, nullable=True, default=datetime.now())
    city_id = Column(Integer, ForeignKey("city.id"))

    city = relationship(City, back_populates="temperatures")
