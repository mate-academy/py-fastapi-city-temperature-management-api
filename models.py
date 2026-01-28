from typing import Optional, List
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    additional_info: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    temperatures: Mapped[List["Temperature"]] = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete"
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id", ondelete="CASCADE")
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    temperature: Mapped[float] = mapped_column(Float)

    city: Mapped["City"] = relationship("City", back_populates="temperatures")
