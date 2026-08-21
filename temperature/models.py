from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from city.models import City


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"))
    date_time: Mapped[datetime] = mapped_column()
    temperature: Mapped[float] = mapped_column()

    city: Mapped[City] = relationship(back_populates="temperatures")

    __table_args__ = (
        UniqueConstraint("city_id", "date_time", name="uq_city_date_time"),
    )
