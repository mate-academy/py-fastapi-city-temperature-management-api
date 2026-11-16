"""SQLAlchemy models for cities and temperature history."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class City(Base):
    """A city tracked by the application."""

    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    additional_info: Mapped[str | None] = mapped_column(Text, nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Temperature(Base):
    """A temperature observation recorded for a city."""

    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        index=True,
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city: Mapped[City] = relationship(back_populates="temperatures")

