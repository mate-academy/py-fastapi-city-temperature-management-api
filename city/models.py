from __future__ import annotations
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from temperature.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True, unique=True)
    additional_info: Mapped[str] = mapped_column(Text, nullable=False)
    temperatures: Mapped[list["Temperature"]] = relationship("Temperature", back_populates="city")
