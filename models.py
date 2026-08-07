from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey, Float
)
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    additional_info = Column(String)
    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete"
    )


class Temperature(Base):
    __tablename__ = 'temperatures'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship("City", back_populates="temperatures")
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
