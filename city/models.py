from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    additional_info: Mapped[str | None] = mapped_column(Text, nullable=True)

    temperatures: Mapped[list["DBTemperature"]] = relationship(
        back_populates="city", cascade="all, delete-orphan"
    )
