from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.temperature import DBTemperature


class DBCity(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    additional_info: Mapped[str | None] = mapped_column(nullable=True)
    temperatures: Mapped[List["DBTemperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan")
