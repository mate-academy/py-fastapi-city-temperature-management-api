from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    additional_info: Mapped[str] = mapped_column(Text, nullable=True)

    temperatures = relationship(
        "Temperature", back_populates="city", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<City {self.name}>"
