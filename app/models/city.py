from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    additional_info: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    latitude: Mapped[float]
    longitude: Mapped[float]

    temperatures = relationship("Temperature", back_populates="city", cascade="all, delete-orphan")
