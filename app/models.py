from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    additional_info = Column(String, nullable=True)

    temperatures = relationship("Temperature", back_populates="city")


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float)

    city = relationship("City", back_populates="temperatures")
