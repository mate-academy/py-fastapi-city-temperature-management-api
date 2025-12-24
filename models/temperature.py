from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    temperature: Mapped[float] = mapped_column(nullable=False)
    city: Mapped["City"] = relationship("City", back_populates="temperatures")
