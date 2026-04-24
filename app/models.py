from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class City(Base):
    __tablename__ = "City"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    additional_info = Column(String, nullable=True)
    temperatures = relationship("Temperature", back_populates="city")

class Temperature(Base):
    __tablename__ = "Temperature"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("City.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)
    city = relationship("City", back_populates="temperatures")
