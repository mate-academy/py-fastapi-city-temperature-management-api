from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from temperatures.models import Temperature


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    additional_info: Mapped[str] = mapped_column(String(255))

    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city"
    )
