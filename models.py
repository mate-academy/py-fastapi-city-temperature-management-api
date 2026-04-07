from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    additional_info: Mapped[str | None] = mapped_column(String(511))

    # PEP 649: forward ref without quotes in py 3.14+
    temperatures: Mapped[list[Temperature]] = relationship(
        back_populates="city", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return self.name


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_time: Mapped[datetime]
    temperature: Mapped[float]

    city: Mapped[City] = relationship(back_populates="temperatures")
