from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from city.models import DBCity
from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship(DBCity)
