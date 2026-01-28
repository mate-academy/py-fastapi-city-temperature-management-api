from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False
    )
    date_time: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    temperature: Mapped[float]
    city: Mapped["City"] = relationship(
        back_populates="temperatures"
    )