from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    additional_info: Mapped[Optional[str]] = mapped_column(
        String(1000), nullable=True
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id"), nullable=False
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
