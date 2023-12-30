from sqlalchemy import  TIMESTAMP, Column, ForeignKey, Integer, String, func
from app.database.db import Base


class UserCodeData(Base):
    __tablename__ = 'users_code_data'
    id = Column(Integer,autoincrement=True, primary_key=True, index=True)
    users_metadata_id = Column(Integer, ForeignKey('users_metadata.id'), nullable=False)
    java = Column(Integer)
    py = Column(Integer)
    js = Column(Integer)
    php = Column(Integer)
    rb = Column(Integer)
    cpp = Column(Integer)
    h = Column(Integer)
    c = Column(Integer)
    cs = Column(Integer)
    html = Column(Integer)
    ipynb = Column(Integer)
    css = Column(Integer)
    ts = Column(Integer)
    kt = Column(Integer)
    dart = Column(Integer)
    m = Column(Integer)
    swift = Column(Integer)
    go = Column(Integer)
    rs = Column(Integer)
    scala = Column(Integer)
    scss = Column(Integer)
    asm = Column(Integer)
    pwn = Column(Integer)
    inc = Column(Integer)
    