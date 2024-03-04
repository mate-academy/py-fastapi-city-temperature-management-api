from sqlalchemy import Column, Integer, String

from db.database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    additional_info = Column(String)
