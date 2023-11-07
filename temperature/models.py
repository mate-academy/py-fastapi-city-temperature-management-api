from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from cities.models import City


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    temperature: Mapped[float] = mapped_column()
    date_time: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE")
    )
    city: Mapped["City"] = relationship(
        back_populates="temperatures", cascade="all, delete"
    )
