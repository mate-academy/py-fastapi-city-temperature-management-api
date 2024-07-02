import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CityModel(Base):
    __tablename__ = "cities"
    id = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    name = Column(String, index=True)
    additional_info = Column(Text, nullable=True)
