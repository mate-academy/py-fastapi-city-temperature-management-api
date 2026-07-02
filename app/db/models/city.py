from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.db.models.base import BaseModel


class CityModel(BaseModel):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    additional_info = Column(String)

    temperature = relationship("TemperatureModel", back_populates="city")
