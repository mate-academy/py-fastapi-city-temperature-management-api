from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import datetime


class City(Base):
    __tablename__ = 'cities'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    additional_info: Mapped[str | None] = mapped_column(nullable=True)
    temperatures: Mapped[list["Temperature"]] = relationship(back_populates="city")


class Temperature(Base):
    __tablename__ = 'temperatures'
    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    date_time: Mapped[datetime.datetime] = mapped_column()
    temperature: Mapped[float] = mapped_column()
    city: Mapped[City] = relationship(back_populates="temperatures")
