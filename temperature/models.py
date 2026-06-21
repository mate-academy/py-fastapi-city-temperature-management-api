import datetime

from sqlalchemy import ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    temperature: Mapped[float] = mapped_column(Float())
    date_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped["City"] = relationship(back_populates="temperature")
