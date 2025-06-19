from sqlalchemy import Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, unique=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    additional_info: Mapped[str] = mapped_column(String(511), nullable=True)

    temperatures = relationship("DBTemperature", back_populates="city")


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, unique=True
    )
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    city = relationship("DBCity", back_populates="temperatures")
