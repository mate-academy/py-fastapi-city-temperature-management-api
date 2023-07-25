from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Text

from pydantic import BaseModel

from database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    additional_info = Column(Text, nullable=True)



class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)
