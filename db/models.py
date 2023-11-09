from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from .engine import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127))
    additional_info = Column(String(255))


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    temperature = Column(Numeric(precision=5, scale=2))
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="temperatures")
