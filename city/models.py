from db.engine import Base
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from custom import intpk

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from temperature.models import Temperature

class City(Base):
    __tablename__ = "cities"
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    additional_info: Mapped[dict] = mapped_column(JSON, nullable=False, unique=True)

    temperatures: Mapped[list["Temperature"]] = relationship(
    back_populates="city",
    cascade="all, delete-orphan",
    )   
