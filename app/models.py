from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    additional_info = Column(String, nullable=True)
    temperatures = relationship(
        "Temperature", back_populates="city", cascade="all, delete-orphan"
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(
        Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False
    )
    date_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
