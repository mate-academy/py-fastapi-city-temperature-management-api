from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)


class Base(DeclarativeBase):
    pass


class CityModel(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    additional_info: Mapped[str]

    temperatures: Mapped[list["TemperatureModel"]] = relationship(
        back_populates="city"
    )


class TemperatureModel(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime]
    temperature: Mapped[float]

    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE")
    )
    city: Mapped["CityModel"] = relationship(
        back_populates="temperatures"
    )
