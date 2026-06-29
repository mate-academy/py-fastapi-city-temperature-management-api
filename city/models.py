from datetime import datetime, timezone

from sqlalchemy import String, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    additional_info: Mapped[str | None] = mapped_column(String(255))
    temperature: Mapped["DBTemperature"] = relationship(
        back_populates="city",
    )


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    city: Mapped["DBCity"] = relationship(
        back_populates="temperature",
    )
