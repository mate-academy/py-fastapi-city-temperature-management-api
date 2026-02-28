from datetime import datetime, UTC
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(211), nullable=False, unique=True)
    additional_info: Mapped[str] = mapped_column(Text, nullable=False)

    temperatures: Mapped[list["DBTemperature"]] = relationship(back_populates="city")


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_time: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    temperature: Mapped[float] = mapped_column(nullable=False)
    city: Mapped["DBCity"] = relationship(back_populates="temperatures")