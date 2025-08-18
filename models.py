from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    additional_info: Mapped[str] = mapped_column()

    temperatures: Mapped[list["Temperature"]] = relationship(back_populates="city")


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))

    date_time: Mapped[datetime] = mapped_column()
    temperature: Mapped[float] = mapped_column()

    city: Mapped["City"] = relationship(back_populates="temperatures")
