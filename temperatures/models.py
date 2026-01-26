from sqlalchemy.orm import relationship

from cities.models import DBCity
from database import Base
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Float
)


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)

    city = relationship(DBCity, back_populates="temperatures")
