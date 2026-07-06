from sqlalchemy import (Column, Integer, String,
                        DateTime, ForeignKey, Float)
from sqlalchemy.orm import relationship

from project.database import Base


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    additional_info = Column(String(511))
    longitude = Column(Float)
    latitude = Column(Float)


class Temperature(Base):
    __tablename__ = 'temperature'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City")
    date_time = Column(DateTime)
    temperature = Column(Float)