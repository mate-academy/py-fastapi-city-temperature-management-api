from sqlalchemy import Column, Integer, String

from database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True, unique=True)
    additional_info = Column(String)
