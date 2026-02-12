from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


if TYPE_CHECKING:
    from temperatures.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    additional_info: Mapped[str | None] = mapped_column(String(511), nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan"
    )
