import datetime
from sqlalchemy import  TIMESTAMP, Column, Date, Integer, String, func
from app.database.db import Base


class UserMetaData(Base):
    __tablename__ = 'users_metadata'
    id = Column(Integer,autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True)
    name = Column(String)
    commits = Column(Integer, default=0)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    lines_code = Column(Integer, default=0)
    lines_tests = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    public_repos = Column(Integer, default=0)
    empty_repos = Column(Integer, default=0)
    forked_repos = Column(Integer, default=0)
    #updated_at = Column(Date, default=Column(Date, datetime.date))