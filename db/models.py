from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(100))
    message_id = Column(String(100))
    user_id = Column(String(50))

    message = Column(Text)
    topic = Column(String(100))
    resolution_department = Column(String(100))
    resolution_text = Column(Text)
    resolution_status = Column(String(50))

    created_at = Column(DateTime, server_default=func.now())
