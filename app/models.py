from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class CityModel(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    additional_info: Mapped[str] = mapped_column()

    temperatures = relationship("TemperatureModel", back_populates="city")


class TemperatureModel(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    date_time: Mapped[datetime] = mapped_column()
    temperature: Mapped[float] = mapped_column()

    city = relationship("CityModel", back_populates="temperatures")
