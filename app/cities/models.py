from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.temperatures.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    additional_info: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )

    temperatures: Mapped[List[Temperature]] = relationship(
        "Temperature", back_populates="city", cascade="all, delete-orphan"
    )
