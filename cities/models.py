from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from database import Base
from temperature.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    additional_info: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )
    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete",
        passive_deletes=True
    )
