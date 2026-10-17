from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Float
from app.database import Base


class City(Base):
    __tablename__ = "City"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    additional_info: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    temperatures: Mapped[list["Temperature"]] = relationship(back_populates="city")

class Temperature(Base):
    __tablename__ = "Temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("City.id"), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    city: Mapped["City"] = relationship(back_populates="temperatures")