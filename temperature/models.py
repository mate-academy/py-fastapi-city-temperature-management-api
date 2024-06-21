from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Float
)

from sqlalchemy.orm import relationship
from city.models import DBCity
from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship(DBCity)
