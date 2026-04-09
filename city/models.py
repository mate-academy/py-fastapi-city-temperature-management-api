from sqlalchemy import Column, Integer, String

from database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    additional_info = Column(String(255))
