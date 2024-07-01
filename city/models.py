from sqlalchemy import Column, Integer, String, Text

from db.engine import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    additional_info = Column(Text, nullable=True)
