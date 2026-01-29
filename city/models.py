from typing import (
    List,
)

from sqlalchemy import (
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from db import Base


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(55),
        unique=True,
        index=True
    )
    additional_info: Mapped[str] = mapped_column(Text)
    temperatures: Mapped[List["Temperature"]] = relationship( # noqa
        back_populates="city"
    )
