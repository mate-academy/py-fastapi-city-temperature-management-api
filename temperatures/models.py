from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    date_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    temperature: Mapped[float] = mapped_column(Float)

    city: Mapped["City"] = relationship(back_populates="temperatures")
