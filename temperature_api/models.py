from datetime import datetime

from sqlalchemy import Integer, ForeignKey, func, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from db.engine import Base


class Temperature(Base):
    __tablename__ = "temperatures"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), index=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    temperature: Mapped[float] = mapped_column(Float)
