import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from engine import Base

if TYPE_CHECKING:
    from cities.models import City


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"))
    date_time: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    temperature: Mapped[float]

    city: Mapped["City"] = relationship(
        back_populates="temperatures",
    )
