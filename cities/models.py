from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class DBCity(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    additional_info: Mapped[str] = mapped_column(String(511))
    temperatures: Mapped[list["DBTemperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan"
    )
