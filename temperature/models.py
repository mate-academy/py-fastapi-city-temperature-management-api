from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Float, Integer, ForeignKey, func

from db.dependencies import Base
from city.models import City


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, default=func.now)
    temperature: Mapped[float] = mapped_column(Float(2))
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("city.id"))
    city: Mapped[City] = relationship(City, back_populates="temperatures")

    def __str__(self) -> str:
        return f"{self.temperature} of city {self.city_id} at {self.date_time}"
