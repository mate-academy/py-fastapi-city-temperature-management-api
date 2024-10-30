from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database.base import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    additional_info = Column(String, nullable=True)

    temperatures = relationship(
        "Temperature", back_populates="city", cascade="all, delete-orphan"
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
