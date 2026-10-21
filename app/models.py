from datetime import datetime, date

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    additional_info: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"),
        nullable=False,
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city: Mapped["City"] = relationship(
        back_populates="temperatures",
    )
