from typing import Optional

from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    additional_info: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    temperatures = relationship("Temperature", back_populates="city", cascade="all, delete-orphan")


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id"), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
