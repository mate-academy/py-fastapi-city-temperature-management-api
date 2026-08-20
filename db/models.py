from db.engine import Base
from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
import datetime


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(511))


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    date_time = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float, nullable=False)
