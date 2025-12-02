from .database import Base
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    additional_info = Column(String)
    temperature = relationship("Temperature", back_populates="city")

class Temperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, index=True, primary_key=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)
    city = relationship("City", back_populates="temperature")
