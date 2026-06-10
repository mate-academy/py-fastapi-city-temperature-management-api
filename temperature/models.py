from db.engine import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from custom import intpk, date_time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from city.models import City

class Temperature(Base):
    __tablename__ = "temperatures"
    id: Mapped[intpk]
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    date_time: Mapped[date_time]
    temperature: Mapped[float] = mapped_column(nullable=False)

    city: Mapped["City"] = relationship(
        back_populates="temperatures"
    )
