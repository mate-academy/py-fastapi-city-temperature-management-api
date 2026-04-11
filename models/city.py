from typing import Optional, List

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from .temperature import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    additional_info: Mapped[Optional[str]] = mapped_column(String)

    temperatures: Mapped[List[Temperature]] = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete"
    )
