from __future__ import annotations
from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.temperature import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    additional_info: Mapped[str | None] = mapped_column(
        String(511),
        nullable=True
    )
    temperatures: Mapped[List[Temperature]] = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan"
    )
