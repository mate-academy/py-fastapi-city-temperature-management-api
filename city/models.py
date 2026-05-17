from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from city.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    additional_info: Mapped[str | None] = mapped_column(Text, nullable=True)
