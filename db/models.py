from __future__ import annotations
from sqlalchemy import String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.engine import Base
import datetime


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    additional_info: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    temperatures: Mapped[list[DBTemperature]] = relationship(
        back_populates="city",
        cascade="all, delete",
        passive_deletes=True
    )

class DBTemperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id",ondelete="CASCADE"),
        nullable=False
    )

    date_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city: Mapped[DBCity] = relationship(back_populates="temperatures")
