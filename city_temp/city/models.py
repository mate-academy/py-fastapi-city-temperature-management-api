from sqlalchemy import Column, Integer, String

from database import Base


class City(Base):
    __tablename__ = "city"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(255), nullable=False, unique=True)
    additional_info: str = Column(String(1000), nullable=False)
