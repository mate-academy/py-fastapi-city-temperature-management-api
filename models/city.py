from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, func, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
	pass


class DBCity(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    additional_info: Mapped[Optional[str]] = mapped_column(String(255))
