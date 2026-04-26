from __future__ import annotations
from sqlalchemy import Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from city.models import City

class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cities.id"),
        nullable=False, index=True
    )
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    cities: Mapped["City"] = relationship("City", back_populates="temperatures")
