from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from city.models import Base


class TemperatureDB(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(String)
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship("CityDB", back_populates="temperatures")
