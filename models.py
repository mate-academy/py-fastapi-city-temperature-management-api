from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, FLOAT
from sqlalchemy.orm import Relationship

from database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(233), index=True)
    additional_info = Column(String(233), index=True)

    temperatures = Relationship("Temperature", back_populates="city")


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'), index=True)
    date_time = Column(DateTime, index=True)
    temperature = Column(FLOAT, index=True)

    cities = Relationship("City", back_populates="temperatures")