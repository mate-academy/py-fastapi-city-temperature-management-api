from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import Base


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(1000), nullable=False)
    temperatures = relationship("DBTemperature", back_populates="city")


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"))
    city = relationship("DBCity", back_populates="temperatures")

