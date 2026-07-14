from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String(255))
    additional_info: Mapped[str] = mapped_column(default="")

    temperatures: Mapped[List["Temperature"]] = relationship(
        back_populates="city", cascade="all, delete-orphan"
    )
