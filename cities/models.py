from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from temperature.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(63))
    description: Mapped[str] = mapped_column()
    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city", lazy="selectin"
    )
