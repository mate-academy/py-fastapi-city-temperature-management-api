from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from city.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    temperature: Mapped[float] = mapped_column(nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))

    city: Mapped["City"] = relationship(back_populates="temperatures")
