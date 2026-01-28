from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    additional_info: Mapped[str] = mapped_column(nullable=True)

    temperature: Mapped[list["Temperature"]] = relationship("Temperature", back_populates="city")
