from sqlalchemy import Column, Integer, String, Text

from src.database import Base


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)
    additional_info = Column(Text, nullable=True)

    def __str__(self):
        return self.name
