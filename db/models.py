from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.engine import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable = False,unique=True)
    additional_info: Mapped[str] = mapped_column(String(1000), nullable = True)


class DBTemperature(Base):
        __tablename__ = "temperature"
        id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
        city_id: Mapped[int] = mapped_column(ForeignKey("city.id"), nullable = False)
        city = relationship(DBCity)
        date_time: Mapped[datetime] = mapped_column(DateTime, nullable = False)
        temperature: Mapped[float] = mapped_column(Float, nullable = False)