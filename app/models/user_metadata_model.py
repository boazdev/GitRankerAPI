import datetime
from sqlalchemy import  TIMESTAMP, Column, Date, DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database.async_sqla_db import Base
from app.models.linkedin_profiles_model import LinkedInProfile

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
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    linkedin_profiles_id = Column(Integer, ForeignKey('profiles.id'), nullable=True)
    linkedin_profile = relationship("LinkedInProfile", back_populates="users_metadata", uselist= False)
    users_code_data = relationship("UserCodeData", back_populates="users_metadata", uselist=False)