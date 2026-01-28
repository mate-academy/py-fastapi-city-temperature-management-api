from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from db.base import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    name: Mapped[str] = mapped_column(
        String(65), nullable=False, unique=True, index=True
    )

    additional_info: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
