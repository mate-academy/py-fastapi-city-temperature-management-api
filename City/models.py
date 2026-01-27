from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


if TYPE_CHECKING:
    from Temperature.models import Temperature


class City(Base):
    __tablename__ = "Cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    additional_info: Mapped[str] = mapped_column(String(300))

    temperatures: Mapped[List["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan"
    )
