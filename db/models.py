from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    additional_info: Mapped[str | None] = mapped_column(nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"))
    city: Mapped[City] = relationship(back_populates="temperatures")
    date_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    temperature: Mapped[float]
