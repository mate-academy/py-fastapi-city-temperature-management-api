from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    additional_info = Column(String, nullable=True)

    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan"
    )

class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(
        Integer,
        ForeignKey("cities.id"),
        nullable=False,
        index=True
    )
    date_time = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
