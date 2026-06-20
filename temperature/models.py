from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime]
    temperature: Mapped[float]
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped["City"] = relationship(back_populates="temperatures")  # type: ignore
