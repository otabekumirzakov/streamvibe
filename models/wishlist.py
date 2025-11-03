from sqlalchemy import Column, Integer
from database import Base

class Wishlist(Base):

    __tablename__ = 'wishlist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    film_id = Column(Integer, nullable=False)