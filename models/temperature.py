from database import Base
from datetime import datetime
from sqlalchemy import ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    date_time: Mapped[datetime] = mapped_column(DateTime)
    temperature: Mapped[float] = mapped_column(Float)
