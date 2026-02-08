import datetime

from sqlalchemy import DateTime, ForeignKey

from database import Base

from sqlalchemy.orm import Mapped, mapped_column


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)
    date_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
    temperature: Mapped[float]
