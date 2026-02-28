from sqlalchemy import String, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from typing import Optional
from datetime import datetime

from database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    additional_info: Mapped[Optional[str]] = mapped_column(String(350), nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan"
    )
    
    @validates("name")
    def validate_name(self, key, value):
        if value is None or len(value) < 3:
            raise ValueError("Name must be at least 3 characters")
        return value


class Temperature(Base):
    __tablename__ = "temperatures"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)
    city: Mapped["City"] = relationship("City", back_populates="temperatures")
