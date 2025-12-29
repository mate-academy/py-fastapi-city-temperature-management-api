from sqlalchemy import Column, Integer, String, ForeignKey, Float, Index, DateTime
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    additional_info = Column(String)

    temperatures = relationship("Temperature", back_populates="city", cascade="all, delete")


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)

    city = relationship("City", back_populates="temperatures")

    __table_args__ = (
        Index("ix_temperature_city_datetime", "city_id", "date_time"),
    )