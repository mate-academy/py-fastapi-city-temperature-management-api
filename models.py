from datetime import date

from sqlalchemy import String, ForeignKey, Date, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import base


class City(base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    additional_info: Mapped[str] = mapped_column(String(511))

    temperatures: Mapped[list["Temperature"]] = relationship(back_populates="city")

class Temperature(base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped["City"] = relationship(back_populates="temperatures")
    date_time: Mapped[date] = mapped_column(Date)
    temperature: Mapped[float] = mapped_column(Float)

