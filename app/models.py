from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class City(Base):
    __tablename__="cities"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(256))
    additional_info: Mapped[str] = mapped_column(String(512), nullable=True)
    temperatures: Mapped[list["Temperature"]] = relationship(back_populates="city")


class Temperature(Base):
    __tablename__ = "temperatures"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["City"] = relationship(back_populates="temperatures")
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    temperature: Mapped[float] = mapped_column(Float)
