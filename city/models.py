from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from temperature.models import DBTemperature


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    additional_info: Mapped[str | None] = mapped_column(String(511))

    temperatures: Mapped[list["DBTemperature"]] = relationship(
        back_populates="city"
    )
