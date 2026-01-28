from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class DBCity(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(65), nullable=False)
    additional_info: Mapped[str] = mapped_column(String(500), nullable=False)
