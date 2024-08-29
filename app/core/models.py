from sqlalchemy import (
    Integer,
    Column,
    String,
    ForeignKey,
    Float,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.core.db import Base


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(511), nullable=False)

    temperatures = relationship(
        "Temperature",
        back_populates="city",
    )


class Temperature(Base):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    city = relationship(City, back_populates="temperatures")
