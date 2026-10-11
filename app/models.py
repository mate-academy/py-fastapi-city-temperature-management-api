from datetime import datetime, timezone

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    additional_info: Mapped[str | None] = mapped_column(String(511))

    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city", cascade="all, delete-orphan"
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), index=True)
    date_time: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    temperature: Mapped[float]

    city: Mapped["City"] = relationship(back_populates="temperatures")
