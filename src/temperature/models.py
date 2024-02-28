from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.city import models
from src.database import Base


class CityTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime)
    temperature = Column(Integer, nullable=False)

    city = relationship(models.City)
