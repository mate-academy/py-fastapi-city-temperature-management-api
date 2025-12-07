from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class DBCity(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(56), nullable=False)
    additional_info: Mapped[str] = mapped_column(String(512), nullable=True)
    temperatures: Mapped[list["DBTemperature"]] = relationship(
        "DBTemperature",
        back_populates="city",
        cascade="all, delete, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.name} ({self.id})"