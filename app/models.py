from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Float, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, unique=True)
    additional_info = Column(String(511))

    temperatures = relationship("Temperature", back_populates="city")

    __table_args__ = (
        UniqueConstraint('name', name='uq_city_name'),
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    date_time = Column(DateTime)
    temperature = Column(Float)

    city = relationship("City", back_populates="temperatures")
