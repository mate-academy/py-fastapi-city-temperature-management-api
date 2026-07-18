from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from cities.models import City


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"),
        nullable=False,
    )

    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    date_time: Mapped[datetime] = mapped_column(nullable=False)

    city: Mapped["City"] = relationship(
        back_populates="temperatures",
    )
