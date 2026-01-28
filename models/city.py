from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[String] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    additional_info: Mapped[String] = mapped_column(
        String(255),
        nullable=True
    )
