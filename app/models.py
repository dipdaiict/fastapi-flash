# Every Models Represnt Table....
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# For Table Creation:
class Post(Base):
    __tablename__ = "posts"

    # Columns Name:
    id  = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)   # By Default it takes True if not provide then...
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))