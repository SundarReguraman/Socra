from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class SessionRequest(BaseModel):
    problem_text: str

class SessionResponse(BaseModel):
    session_id: UUID
    role: str
    content: str
    hint_level: int
    session_status: str

class MessageRequest(BaseModel):
    content: str

class MessageResponse(BaseModel):
    role: str
    content: str
    hint_level: int
    session_status: str

class MessageModel(BaseModel):
    role: str
    content: str
    created_at: datetime

class SessionHistoryResponse(BaseModel):
    session_id: UUID
    problem_text: str
    status: str
    messages: list[MessageModel]

