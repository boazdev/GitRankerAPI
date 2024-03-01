from sqlalchemy import  TIMESTAMP, Column, ForeignKey, Integer, String, func
from app.database.async_sqla_db import Base
from sqlalchemy.orm import relationship

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

    # Newly added columns
    scss_repositories = Column(Integer, default=0)
    assembly_repositories = Column(Integer, default=0)
    pawn_repositories = Column(Integer, default=0)
    objectivec_repositories = Column(Integer, default=0)
    kotlin_repositories = Column(Integer, default=0)
    dart_repositories = Column(Integer, default=0)
    c_repositories = Column(Integer, default=0)
    typescript_repositories = Column(Integer, default=0)
    html_repositories = Column(Integer, default=0)
    java_repositories = Column(Integer, default=0)
    ejs_repositories = Column(Integer, default=0)
    csharp_repositories = Column(Integer, default=0)
    javascript_repositories = Column(Integer, default=0)
    jupyter_repositories = Column(Integer, default=0)
    cpp_repositories = Column(Integer, default=0)
    css_repositories = Column(Integer, default=0)
    python_repositories = Column(Integer, default=0)
    nodejs_repositories = Column(Integer, default=0)
    angular_repositories = Column(Integer, default=0)
    react_repositories = Column(Integer, default=0)
    dotnet_repositories = Column(Integer, default=0)
    php_repositories = Column(Integer, default=0)
    ruby_repositories = Column(Integer, default=0)
    scala_repositories = Column(Integer, default=0)
    swift_repositories = Column(Integer, default=0)
    go_repositories = Column(Integer, default=0)
    r_repositories = Column(Integer, default=0)
    rust_repositories = Column(Integer, default=0)

    users_metadata = relationship("UserMetaData", back_populates="users_code_data")
    