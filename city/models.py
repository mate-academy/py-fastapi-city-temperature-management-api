import datetime

from sqlalchemy import String, ForeignKey, DateTime, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.database import Base




class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    additional_info: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    temperatures = relationship("Temperature", back_populates="city")


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    temperature: Mapped[float] = mapped_column(Float)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city = relationship("City", back_populates="temperatures")