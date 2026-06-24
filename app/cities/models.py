from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    additional_info: Mapped[str | None] = mapped_column(default=None)

    temperatures: Mapped[List["Temperature"]] = relationship(
        "Temperature", back_populates="city", cascade="all, delete-orphan"
    )
