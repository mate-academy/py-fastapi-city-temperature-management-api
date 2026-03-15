from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    additional_info = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    temperatures = relationship("Temperature", back_populates="city", cascade="all, delete")


class Temperature(Base):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float)
    city = relationship("City", back_populates="temperatures")
