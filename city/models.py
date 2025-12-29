from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.engine import Base
from sqlalchemy import String


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    additional_info: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )

    temperature = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan"
    )
