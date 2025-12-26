from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, DateTime, Float
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from database.mixins import IdMixin


class Base(DeclarativeBase):
    pass


class CityModel(Base, IdMixin):
    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(String)
    additional_info: Mapped[str] = mapped_column(String, nullable=True)
    temperatures: Mapped[List["Temperature"]] = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan"
    )


class Temperature(Base, IdMixin):
    __tablename__ = "temperatures"

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    city: Mapped["CityModel"] = relationship("CityModel", back_populates="temperatures")

    date_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.now)
    temperature: Mapped[float] = mapped_column(Float, nullable=True)
