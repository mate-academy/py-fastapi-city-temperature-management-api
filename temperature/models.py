from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class DBTemperature(Base):
    __tablename__ = "temperatures"
    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["DBCity"] = relationship(back_populates="temperatures")
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    temperature: Mapped[float] = mapped_column(Float(precision=4))
