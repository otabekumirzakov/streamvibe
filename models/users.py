from sqlalchemy import Column, String, Integer
from database import Base

class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False)
    image = Column(String(255), nullable=False)