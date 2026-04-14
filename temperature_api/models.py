from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    date_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    temperature: Mapped[float] = mapped_column(Float)
