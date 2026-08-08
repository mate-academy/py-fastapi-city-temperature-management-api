from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.engine import Base

class City(Base):
    __tablename__ = 'cities'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    additional_info: Mapped[str | None] = mapped_column(String, nullable=True)
