from sqlalchemy import String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class CityModel(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    additional_info: Mapped[str] = mapped_column(Text, nullable=False)
