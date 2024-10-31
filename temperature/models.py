from sqlalchemy import Column, Integer, Float, func, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from city.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False, default=func.now())
    temperature = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)

    city = relationship(City, back_populates="temperatures")
