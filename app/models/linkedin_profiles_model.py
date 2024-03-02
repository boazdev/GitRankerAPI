from sqlalchemy import  TIMESTAMP, Column, ForeignKey, Integer, String, func
from app.database.async_sqla_db import Base
from sqlalchemy.orm import relationship

class LinkedInProfile(Base):
    __tablename__ = 'profiles'
    id = Column('id',Integer,autoincrement=True, primary_key=True, index=True)
    url = Column(String, nullable=False)
    open_to_work = Column(String)
    current_employment = Column(String)
    location = Column(String)
    talent_id = Column(String)
    industry = Column(String)
    name = Column(String)
    location = Column(String)
    status = Column(String)
    users_metadata = relationship("UserMetaData", back_populates="linkedin_profile")
