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


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)


class DBCity(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    additional_info = Column(String(500))

    temperatures = relationship("DBTemperature", back_populates="city")
