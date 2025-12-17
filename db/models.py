import datetime
from sqlalchemy import String, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(251), unique=True, nullable=False)
    additional_info: Mapped[str] = mapped_column(String(551), nullable=False)

    temperatures: Mapped[list["DBTemperature"]] = relationship(
        back_populates="city",
    )


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped["DBCity"] = relationship(back_populates="temperatures")
    date_time: Mapped[datetime.date] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
