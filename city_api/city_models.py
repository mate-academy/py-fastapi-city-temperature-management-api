from sqlalchemy import Column, Integer, String, Date

from db.database import Base


class DBCity(Base):
    __tablename__ = "City"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(512), nullable=True)
