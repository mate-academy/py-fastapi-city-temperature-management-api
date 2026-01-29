from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    additional_info: Mapped[str] = mapped_column(String(300), nullable=True)
