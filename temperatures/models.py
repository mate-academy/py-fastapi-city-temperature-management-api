from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from cities.models import City


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"), nullable=False
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city: Mapped["City"] = relationship(back_populates="temperatures")
