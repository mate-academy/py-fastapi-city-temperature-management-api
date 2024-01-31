from sqlalchemy import Column, Integer, String

from database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    additional_info = Column(String(511), nullable=True)
