from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from temperature_app.database import Base


class CityModel(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    additional_info = Column(String(511), nullable=True)

    temperatures = relationship("TemperatureModel", back_populates="city")


class TemperatureModel(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    temperature = Column(Float, nullable=False)
    date_time = Column(DateTime, nullable=False)

    city = relationship("CityModel", back_populates="temperatures")
