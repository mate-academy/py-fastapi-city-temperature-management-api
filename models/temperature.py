from datetime import datetime

from sqlalchemy import DateTime, func, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from models.city import Base


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    temperature: Mapped[float | int] = mapped_column(Float)
