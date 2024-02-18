from database import Base
from sqlalchemy import Column, Integer, String


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(255), nullable=True)
