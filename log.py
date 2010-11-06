from sqlalchemy import Column, Integer, String, Float
from db import Base, db_session

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    video_hash = Column(String)
    vote = Column(String)

    def __init__(self, username, video_hash, vote):
        self.username = username
        self.video_hash = video_hash
        self.vote = vote

class Scrob(Base):
    __tablename__ = 'scrobs'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    video_hash = Column(String)
    remaining_secs = Column(Float)

    def __init__(self, username, video_hash, remaining_secs):
        self.username = username
        self.video_hash = video_hash
        self.remaining_secs = remaining_secs

class Query(Base):
    __tablename__ = 'queries'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    query = Column(String)
    offset = Column(Integer)

    def __init__(self, username, query, offset):
        self.username = username
        self.query = query
        self.offset = offset

