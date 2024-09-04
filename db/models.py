import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from db.engine import Base


class DBCity(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(1000), nullable=True)


class DBTemperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"), onupdate="CASCADE", nullable=False)
    city = relationship(DBCity)
    date_time = Column(DateTime, default=datetime.datetime.now)
    temperature = Column(Float, nullable=False)
