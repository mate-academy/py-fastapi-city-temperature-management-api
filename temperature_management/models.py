from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    additional_info: Mapped[str] = mapped_column(String(255))
    temperatures: Mapped[list["DBTemperature"]] = relationship(
        back_populates="city"
    )


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    temperature: Mapped[float] = mapped_column()
    date_time: Mapped[datetime] = mapped_column()
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"), nullable=True)
    city: Mapped[DBCity | None] = relationship(back_populates="temperatures")
