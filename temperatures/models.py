from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"
    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    date_time: Mapped[datetime] = mapped_column(DateTime())
    temperature: Mapped[float] = mapped_column(Float())
