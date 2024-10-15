from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    additional_info = Column(String(500), nullable=True)

    city_temperature = relationship("DBTemperature", back_populates="city")


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False, index=True)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)

    city = relationship("DBCity", back_populates="city_temperature")
