from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from city.models import DBCity
from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id_ = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)

    city = relationship(DBCity)
