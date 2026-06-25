from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TemperatureModel(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE")
    )
    date_time: Mapped[datetime] = mapped_column(DateTime)
    temperature: Mapped[float] = mapped_column(Float)
