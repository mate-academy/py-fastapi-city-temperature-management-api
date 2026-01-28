from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class City(Base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(100),
        index=True)
    additional_info: Mapped[str] = mapped_column(String(512), nullable=False)
    temperatures: Mapped[List["Temperature"]] = relationship(
        back_populates="city")