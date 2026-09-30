from datetime import date

from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    additional_info: Mapped[str] = mapped_column(String(255))


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey
        (
        "cities.id",
        ondelete="CASCADE"
        )
    )
    date_time: Mapped[date] = mapped_column(Date, nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
