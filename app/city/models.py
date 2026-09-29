from typing import List, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    additional_info: Mapped[Optional[str]] = mapped_column(Text)

    temperatures: Mapped[List["Temperature"]] = relationship(  # noqa: F821
        back_populates="city",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
