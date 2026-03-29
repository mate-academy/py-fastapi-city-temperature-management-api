from __future__ import annotations
from typing import TYPE_CHECKING
import datetime

from sqlalchemy import func, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.database import Base

if TYPE_CHECKING:
    from .city import City


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    temperature: Mapped[float] = mapped_column(
        Numeric(precision=6, scale=2), nullable=False
    )
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["City"] = relationship(back_populates="temperatures")

    def __repr__(self) -> str:
        return f"Temperature(id={self.id}, temperature={self.date_time})"
