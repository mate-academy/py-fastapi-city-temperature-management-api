from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class City(Base):
    """Represents a city in the database."""

    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    additional_info: Mapped[str | None] = mapped_column(String(511), nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(back_populates="city") #noqa
