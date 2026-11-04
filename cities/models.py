from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
# from temperatures.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    additional_info: Mapped[str] = mapped_column(String(300), nullable=False)

    temperature: Mapped[Optional["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan"
    )
