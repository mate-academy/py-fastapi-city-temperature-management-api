from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float
)

from db.database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    additional_info = Column(String)

    temperatures = relationship("Temperature", back_populates="city")


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="temperatures")
