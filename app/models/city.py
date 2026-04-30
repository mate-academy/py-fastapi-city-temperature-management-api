from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.temperature import DBTemperature


class DBCity(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    additional_info: Mapped[Optional[str]] = mapped_column(String(510))

    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    temperatures: Mapped[list["DBTemperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )
