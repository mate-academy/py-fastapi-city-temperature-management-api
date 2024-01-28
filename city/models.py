from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from database import Base
from datetime import datetime


class DBCity(Base):
    __tablename__ = "City"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True)
    additional_info = Column(String(500))


# class DBTemperature(Base):
#     __tablename__ = "Temperature"
#
#     id = Column(Integer, primary_key=True, index=True)
#     city_id = Column(Integer, ForeignKey("City.id"))
#     data_time = Column(DateTime, default=datetime.utcnow, nullable=True)
#     temperature = Column(Float)