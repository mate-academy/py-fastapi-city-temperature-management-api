from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.city import City


class Temperature(Base):
    __tablename__ = 'temperatures'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey(
            'cities.id',
            ondelete="CASCADE"
        )
    )
    city: Mapped[City] = relationship(
        "City",
        back_populates="temperatures"
    )
    date_time: Mapped[datetime] = mapped_column()
    temperature: Mapped[float] = mapped_column()
