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


class CityDB(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), unique=True, nullable=False)
    additional_info = Column(Text)

    temperatures = relationship(

        "TemperatureDB",
        cascade="all, delete-orphan",
        back_populates="city"
    )


class TemperatureDB(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, default=func.now(), nullable=False)
    temperature = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"))

    city = relationship("CityDB", back_populates="temperatures")
