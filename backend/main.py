from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone
from strategy_engine import get_next_response
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db
import models
import schemas

models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Socra AI Reasoning Coach API", version ="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["https://localhost:5174"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Socra Backend is running successfully!"}

@app.post("/v1/session", response_model =schemas.SessionResponse, status_code =status.HTTP_201_CREATED)
def create_session(request: schemas.SessionRequest, db: Session = Depends(get_db)):
    
    new_session = models.Session(
        problem_text = request.problem_text,
        current_hint_level = 1,
        status = "active"
    ) 

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    first_question = get_next_response(
        problem_text = request.problem_text,
        messages = [],
        hint_level= 1
    )

    first_message = models.Message(
        session_id = new_session.id,
        sender = "coach",
        content = first_question,
        hint_level_at_time = 1
    )

    db.add(first_message)
    db.commit()



    return {
        "session_id": new_session.id,
        "role": "coach",
        "content": first_question,
        "hint_level": new_session.current_hint_level,
        "session_status": new_session.status
    }



@app.get("/v1/session/{id}", response_model = schemas.SessionHistoryResponse, status_code = status.HTTP_200_OK)
def retrieve_session(id: UUID, db: Session = Depends(get_db)):
    session_record = db.query(models.Session).filter(models.Session.id == id).first()

    if not session_record:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail =f"Session with id {id} was not found"
        )
    
    return session_record

@app.post("/v1/session/{id}/message", response_model = schemas.MessageResponse, status_code = status.HTTP_200_OK )
def send_message(id: UUID, request: schemas.MessageRequest, db: Session = Depends(get_db)):
    session_record = db.query(models.Session).filter(models.Session.id == id).first()

    if not session_record:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Session not found"

        )




    user_message = models.Message(
        session_id = id,
        sender = "user",
        content = request.content,
        progress_score = 0,
        hint_level_at_time = session_record.current_hint_level, 
        created_at = datetime.now(timezone.utc)

    )

    db.add(user_message)

    #Get the Entire Conversation_History
    messages = db.query(models.Message).filter(models.Message.id == id).order_by(models.Message.created_at).all()
    socra_response = get_next_response(
        problem_text = session_record.problem_text,
        messages= messages,
        hint_level = session_record.current_hint_level
    )

    #Get next Response from Strategy Engine
    socra_message = models.Message(
        session_id = id,
        sender = "coach",
        content = socra_response,
        progress_score = None,
        hint_level_at_time = session_record.current_hint_level,
        created_at = datetime.now(timezone.utc)
    )

    db.add(socra_message)
    db.commit()
    

    return{
        "role":"coach",
        "content":socra_response,
        "hint_level": session_record.current_hint_level,
        "session_status":"active"

    }






     
