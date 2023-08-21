from sqlalchemy import Column, String, Integer

from database import Base


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    additional_info = Column(String, nullable=True)
