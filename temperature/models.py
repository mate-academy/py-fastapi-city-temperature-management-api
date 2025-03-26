from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from database import Base


class TemperatureDB(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime, default=func.now(), onupdate=func.now())
    temperature = Column(String(255), nullable=False)

    city = relationship("CityDB", back_populates="temperatures")
