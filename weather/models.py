from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(511), nullable=False)


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    date_time = Column(DateTime, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"))

    city = relationship(City)
