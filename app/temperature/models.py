from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class Temperature(Base):
    """Represents a temperature record for a city."""

    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"), nullable=False
    )  # FIX: Changed "city.id" to "cities.id"
    city: Mapped["City"] = relationship(back_populates="temperatures") #noqa

    __table_args__ = (
        UniqueConstraint("city_id", "date_time", name="unique_city_datetime"),
    )
