import datetime


from sqlalchemy import String, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class City(Base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    additional_info: Mapped[str] = mapped_column(String(511))
    temperatures: Mapped[list["Temperature"]] = relationship(back_populates="city")

class Temperature(Base):
    __tablename__ = "temperature"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_time: Mapped[datetime.date] = mapped_column(DateTime)
    temperature: Mapped[float] = mapped_column(Float)
    city: Mapped["City"] = relationship(back_populates="temperatures")
