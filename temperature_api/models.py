from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base


class TemperatureModels(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    city = relationship('CityModels', back_populates="temperature")
