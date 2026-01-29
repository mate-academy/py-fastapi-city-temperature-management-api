from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.temperatures.models import Temperature
from app.db.base import Base

class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    additional_info: Mapped[str | None] = mapped_column(String, nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city",
        cascade="all, delete",
        lazy="selectin"
    )