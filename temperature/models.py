import datetime

from pydantic import BaseModel
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from city.models import DBCity


class DBTemperature(BaseModel):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped[DBCity] = relationship(back_populates="temperature")
    date_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(default=0, nullable=False)