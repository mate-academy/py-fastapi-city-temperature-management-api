from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from sqlalchemy import String
from src.temperature.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    additional_info: Mapped[str] = mapped_column(String(255))

    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city", cascade="all, delete-orphan"
    )
