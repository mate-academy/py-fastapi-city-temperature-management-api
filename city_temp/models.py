from datetime import datetime
from typing import List

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship
)

from database import Base


class DBCity(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    additional_info: Mapped[
        str | None
    ] = mapped_column(
        String(511),
        nullable=True,
    )
    temperatures: Mapped[List["DBTemperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"),
        nullable=False,
        index=True
    )
    city: Mapped["DBCity"] = relationship(
        back_populates="temperatures"
    )
