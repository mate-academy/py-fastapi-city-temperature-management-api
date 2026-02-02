from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.temperature import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    additional_info: Mapped[str | None] = mapped_column(Text, nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
