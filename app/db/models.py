from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from db.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class CityORM(Base):
    __tablename__ = "cities"
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(256), unique=True)
    additional_info: Mapped[str | None] = mapped_column(String(512), nullable=True)

    temperatures: Mapped[list["TemperatureORM"]] = relationship(
        back_populates="city", cascade="all, delete-orphan"
    )

class TemperatureORM(Base):
    __tablename__ = "temperature"
    id: Mapped[intpk]
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE")
    )
    date_time: Mapped[datetime]
    
    temperature: Mapped[float] = mapped_column(nullable=True)

    city: Mapped["CityORM"] = relationship(back_populates="temperatures")
