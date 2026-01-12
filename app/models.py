from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DBCity(Base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    additional_info: Mapped[str] = mapped_column(String(511), nullable=True)
    temperatures: Mapped[list["DBTemperature"]] = relationship(
        back_populates="city", cascade="all, delete-orphan"
    )


class DBTemperature(Base):
    __tablename__ = "temperature"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    temperature: Mapped[float] = mapped_column(Float)

    city: Mapped["DBCity"] = relationship(back_populates="temperatures")
