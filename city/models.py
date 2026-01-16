from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    additional_info: Mapped[str] = mapped_column(String(255), nullable=True)
    temperatures: Mapped[list["Temperature"]] = relationship(
        "temperature.models.Temperature",
        back_populates="city",
        cascade="all, delete-orphan",
        lazy="select"
    )
