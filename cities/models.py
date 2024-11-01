from database import Base
from sqlalchemy import Column, Integer, String


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    additional_info = Column(String(250), nullable=True)
