from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date_time: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), nullable=False
    )
    temperature: Mapped[float] = mapped_column(nullable=False)

    city: Mapped["City"] = relationship(back_populates="temperatures")  # noqa: F821
