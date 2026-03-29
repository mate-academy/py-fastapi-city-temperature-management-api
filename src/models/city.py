from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base

if TYPE_CHECKING:
    from .temperature import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    additional_info: Mapped[Optional[str]] = mapped_column(
        String(63), nullable=False, default=""
    )

    temperatures: Mapped[List["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"City(id={self.id}, name={self.name})"
