from sqlalchemy import Column, Integer, String

from settings import Base


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(511))
