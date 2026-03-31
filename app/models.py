# from typing import Text
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
