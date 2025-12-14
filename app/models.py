from typing import List
from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    additional_info: Mapped[str] = mapped_column(String(500), nullable=True)
    temperatures: Mapped[List["DBTemperature"]] = relationship(back_populates="city")



class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_time: Mapped[datetime] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    city: Mapped["DBCity"] = relationship(back_populates="temperatures")
