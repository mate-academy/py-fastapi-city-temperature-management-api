from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

class DBCity(Base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50),unique=True, nullable=False)
    additional_info: Mapped[str] = mapped_column(String(255),nullable=True)
    temperatures = relationship("DBTemperature")


class DBTemperature(Base):
    __tablename__ = "temperature"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("city.id"), index=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False, )
