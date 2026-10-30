from sqlalchemy import Integer, String, Column

from database import Base


class DBCity(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    additional_info = Column(String(550))
