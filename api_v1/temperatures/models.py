from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api_v1.models import Base

if TYPE_CHECKING:
    from api_v1.cities.models import City


class Temperature(Base):
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    date_time: Mapped[datetime]
    temperature: Mapped[float]
    city: Mapped["City"] = relationship(back_populates="temperatures")

    def __repr__(self) -> str:
        return f"{self.date_time}: {self.temperature}"
