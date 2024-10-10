from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .engine import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    additional_info: Mapped[str] = mapped_column()
    temperatures: Mapped[list["Temperature"]] = relationship("Temperature", back_populates="city")


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)
    city: Mapped[City] = relationship(City, back_populates="temperatures")
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    temperature: Mapped[float] = mapped_column()
