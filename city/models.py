from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.dependencies import Base


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    additional_info: Mapped[str] = mapped_column(String(500))
    temperatures: Mapped[list["Temperature"]] = relationship(
        "Temperature", back_populates="city"
    )

    def __str__(self) -> str:
        return self.name
