from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["DBCity"] = relationship("DBCity",back_populates="temperatures")
    date_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"{self.date_time}, {self.city.name} --- {self.temperature}"