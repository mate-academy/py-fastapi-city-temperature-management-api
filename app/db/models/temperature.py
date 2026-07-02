from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from app.db.models.base import BaseModel


class TemperatureModel(BaseModel):
    __tablename__ = 'temperature'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    date_time = Column(DateTime)
    temperature = Column(Float)

    city = relationship("CityModel", back_populates="temperature")
