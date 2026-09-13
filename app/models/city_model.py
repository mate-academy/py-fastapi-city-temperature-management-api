from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from app.models.temperature_model import DBTemperature


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    additional_info: Mapped[str] = mapped_column(String(511), nullable=False)

    temperatures: Mapped[list["DBTemperature"]] = relationship(
        back_populates="city"
    )
