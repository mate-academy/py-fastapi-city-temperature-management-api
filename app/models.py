from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    additional_info: Mapped[str | None] = mapped_column(String(500), nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(
        "Temperature", back_populates="city", cascade="all, delete-orphan"
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id"), nullable=False, index=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city: Mapped["City"] = relationship("City", back_populates="temperatures")
