import datetime

from typing import List
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class City(Base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(255), nullable=False)
    additional_info: Mapped[str] = mapped_column(String(), nullable=True)

    temperatures: Mapped[List["Temperature"]] = relationship(
        back_populates="city", cascade="all, delete-orphan")


class Temperature(Base):
    __tablename__ = "temperature"
    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True)
    temperature: Mapped[float]

    city: Mapped["City"] = relationship(back_populates="temperatures")
