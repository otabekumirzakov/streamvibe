from sqlalchemy import Column, String, Integer
from database import Base

class Crew(Base):
    __tablename__ = "crew"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    image = Column(String(95), nullable=False)
    role = Column(String(20), nullable=False)