from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    additional_info: Mapped[str | None] = mapped_column(String(300))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan"
    )
