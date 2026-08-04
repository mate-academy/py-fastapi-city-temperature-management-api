from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column()

    additional_info: Mapped[str | None] = mapped_column(
        nullable=True,
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"),
    )

    date_time: Mapped[datetime] = mapped_column()

    temperature: Mapped[float] = mapped_column()
