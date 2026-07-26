from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from temperature.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    additional_info: Mapped[str] = mapped_column(String(255), nullable=True)
    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
