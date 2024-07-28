from __future__ import annotations
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import String, Text

from src.database import Base


class City(Base):
    __tablename__ = "city"
    name = mapped_column(String(150), nullable=False)
    additional_info = mapped_column(Text, nullable=True)

    def __repr__(self):
        return self.name
