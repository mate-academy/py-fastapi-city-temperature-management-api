from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    additional_info = Column(String, nullable=True)

    # Relationship to access temperatures easily
    temperatures = relationship("Temperature", back_populates="city", cascade="all, delete")

class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    temperature = Column(Float)

    city = relationship("City", back_populates="temperatures")
