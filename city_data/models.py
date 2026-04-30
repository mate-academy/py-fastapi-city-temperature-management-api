import datetime

from sqlalchemy import String, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class City(Base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    additional_info: Mapped[str] = mapped_column(String(255))


class Temperature(Base):
    __tablename__ = "temperature"
    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey(City.id), nullable=False)
    date_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    temperature: Mapped[float] = mapped_column(Float)
