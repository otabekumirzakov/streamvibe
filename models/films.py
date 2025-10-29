from sqlalchemy import Column, String, Integer, JSON, Text
from database import Base


class Films(Base):
    __tablename__ = "films"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    video_url = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    languages = Column(JSON, nullable=False)
    genres = Column(JSON, nullable=False)
    view = Column(Integer, default=0)