from database import Base
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from cities.models import City


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime(timezone=True), server_default=func.now())
    temperature = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship(City)
