from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    additional_info = Column(String, nullable=True)

    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete, delete-orphan",
    )


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    date_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
