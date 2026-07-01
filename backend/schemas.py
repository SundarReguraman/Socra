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
    id: UUID
    sender: str
    content: str
    hint_level_at_time: Optional[int]
    progress_score: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class SessionHistoryResponse(BaseModel):
    id: UUID
    problem_text: str
    current_hint_level: int
    status: str
    created_at: datetime
    messages: list[MessageModel]

    class Config:
        from_attributes = True
        

