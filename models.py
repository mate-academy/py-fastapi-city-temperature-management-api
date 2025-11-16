from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class City(Base):
    tablename = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    additional_info = Column(String, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan"
    )


class Temperature(Base):
    tablename = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
