from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Float,
    func
)
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    additional_info = Column(Text)

    temperatures = relationship(
        "Temperature", cascade="all, delete-orphan", back_populates="city"
    )


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime, nullable=False, default=func.now())
    temperature = Column(Float, nullable=False)

    city = relationship(City, back_populates="temperatures")
