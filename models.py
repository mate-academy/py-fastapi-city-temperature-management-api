from datetime import datetime
from sqlalchemy import String, Float, ForeignKey,  DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship # type: ignore
from database import Base


class DBCity(Base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    additional_info: Mapped[str] = mapped_column(String(511), nullable=False)
    temperatures: Mapped[list["DBTemperature"]] = relationship(
        "DBTemperature", back_populates="city",
        cascade="all, delete"
    )

class DBTemperature(Base):
    __tablename__ = "temperature"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    city: Mapped["DBCity"] = relationship("DBCity", back_populates="temperatures")