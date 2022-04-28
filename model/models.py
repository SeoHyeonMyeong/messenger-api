from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title= Column(String, nullable=False)
    content= Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


