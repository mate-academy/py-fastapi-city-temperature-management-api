from sqlalchemy import ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from city.models import DBCity
from database import Base


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)

    city: Mapped["DBCity"] = relationship(back_populates="temperatures")
