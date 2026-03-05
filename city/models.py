from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    additional_info: Mapped[str] = mapped_column(nullable=True)
    temperatures: Mapped[list["Temperature"]] = relationship(
        "Temperature",
        back_populates="city",
    )
