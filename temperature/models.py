from database import Base

from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from city.models import City


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"))

    city = relationship(City)
