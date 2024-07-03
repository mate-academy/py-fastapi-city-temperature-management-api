from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float
)
from sqlalchemy.orm import relationship

from database import Base


class DBCity(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    additional_info = Column(String(255))

    temperatures = relationship("DBTemperature", back_populates="city")


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), index=True)
    date_time = Column(DateTime, index=True)
    temperature = Column(Float)

    city = relationship(DBCity, back_populates="temperatures")
