from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from temperature.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    additional_info: Mapped[str] = mapped_column(Text)

    temperatures: Mapped[list[Temperature]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )
