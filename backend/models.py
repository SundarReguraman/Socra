from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid = True), primary_key = True, default= uuid.uuid4)
    name = Column(String, nullable = False)
    email = Column(String, nullable = False)
    auth_provider = Column(String, nullable = False)
    signup_time = Column(DateTime, nullable= False, default = lambda: datetime.now(timezone.utc))

class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    user_id = Column(UUID(as_uuid = True),ForeignKey("users.id"), nullable = True)
    problem_text = Column(Text, nullable = False)
    current_hint_level = Column(Integer, nullable = False, default = 1)
    consecutive_stuck = Column(Integer, nullable = True, default = 0)
    status = Column(String, nullable = False, default = "active")
    created_at = Column(DateTime, nullable = False, default = lambda: datetime.now(timezone.utc))

    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid = True), primary_key= True, default= uuid.uuid4)
    session_id = Column(UUID(as_uuid = True), ForeignKey("sessions.id"), nullable = False)
    sender = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    progress_score = Column(Integer, nullable = True)
    hint_level_at_time = Column(Integer, nullable = True)
    created_at = Column(DateTime, nullable = False, default = lambda: datetime.now(timezone.utc))

    session = relationship("Session", back_populates = "messages")
    




