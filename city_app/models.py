from datetime import datetime
from typing import List

from sqlalchemy.sql import func
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class City(Base):

    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    additional_info: Mapped[str] = mapped_column(String(1020), nullable=True)
    temperatures: Mapped[List["Temperature"]] = relationship(back_populates="city", cascade="all, delete, delete-orphan")


class Temperature(Base):

    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    temperature: Mapped[float] = mapped_column()

    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped[City] = relationship(back_populates="temperatures")

    def __repr__(self):
        return f"<Temperature(date_time={self.date_time}, temperature={self.temperature})>"
