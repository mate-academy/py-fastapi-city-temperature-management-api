from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

# Імпортуємо Base з нашого файлу database.py
from database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    additional_info = Column(String, nullable=True)

    # Зв'язок з температурами. cascade="all, delete" видаляє температури, якщо видаляється місто
    temperatures = relationship("Temperature", back_populates="city", cascade="all, delete-orphan")

class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float)

    city = relationship("City", back_populates="temperatures")