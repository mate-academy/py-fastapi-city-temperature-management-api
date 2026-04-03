from typing import List
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

class City(Base):
    __tablename__ = "city"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    additional_info: Mapped[str] = mapped_column(Text)

    temperatures: Mapped[List["Temperature"]] = relationship(back_populates="city", order_by="Temperature.date_time.desc()")
