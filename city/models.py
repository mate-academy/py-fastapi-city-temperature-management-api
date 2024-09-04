from sqlalchemy import Integer, Column, String

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    additional = Column(String)
