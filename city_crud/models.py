from typing import Optional

from sqlalchemy import Column, Integer, String

from db import engine


Base = engine.Base


class City(Base):
    __tablename__ = "cities"

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    name: str = Column(String(128), unique=True, nullable=False, index=True)
    additional_info: Optional[str] = Column(String(255), unique=False, nullable=True)
