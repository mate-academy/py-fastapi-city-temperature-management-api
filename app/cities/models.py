from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    additional_info: Mapped[str | None] = mapped_column(Text, nullable=True)

    temperatures = relationship(
        "Temperature", back_populates="city", cascade="all, delete-orphan"
    )
