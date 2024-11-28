from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float

from app.database import Base


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    additional_info = Column(String, nullable=False)


class Temperature(Base):
    __tablename__ = 'temperature'

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    date_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    temperature = Column(Float, nullable=False)
