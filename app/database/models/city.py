from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    additional_info: Mapped[str | None] = mapped_column(String(255), nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(  # noqa: F821
        back_populates="city", cascade="all, delete-orphan"
    )
