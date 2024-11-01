from database import Base
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Float
)
from sqlalchemy.orm import relationship
from cities.models import City


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    temperature = Column(Float, nullable=False)
    date_time = Column(DateTime, nullable=False)

    city = relationship(City)
