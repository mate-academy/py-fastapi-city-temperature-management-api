from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from sqlalchemy import DateTime, Float

from city.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    name: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )
    additional_info: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city"
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"),
        nullable=False,
    )

    date_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    city: Mapped["City"] = relationship(
        back_populates="temperatures"
    )
