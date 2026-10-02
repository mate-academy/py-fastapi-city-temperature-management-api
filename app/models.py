from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import Float, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    additional_info: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    temperatures: Mapped[List["Temperature"]] = relationship(
        "Temperature", back_populates="city", cascade="all, delete-orphan"
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)

    date_time: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city: Mapped["City"] = relationship("City", back_populates="temperatures")
