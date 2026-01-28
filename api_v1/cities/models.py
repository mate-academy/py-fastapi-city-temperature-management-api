from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from api_v1.models import Base

if TYPE_CHECKING:
    from api_v1.temperatures.models import Temperature


class City(Base):
    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(unique=True)
    additional_info: Mapped[str | None]
    temperatures: Mapped[list["Temperature"]] = relationship(
        back_populates="city", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return self.name
