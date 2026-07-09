from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text
from uuid import UUID
from auth import verify_user
from datetime import datetime, timezone
from strategy_engine import get_next_response
from fastapi.middleware.cors import CORSMiddleware
from session_service import get_session_with_messages, store_message
from progress_evaluator import evaluate_progress
from database import engine, get_db
import models
import schemas

models.Base.metadata.create_all(bind=engine)


def ensure_session_schema() -> None:
    inspector = inspect(engine)
    if not inspector.has_table("sessions"):
        return

    session_columns = {column["name"] for column in inspector.get_columns("sessions")}
    if "consecutive_stuck" not in session_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE sessions ADD COLUMN consecutive_stuck INTEGER DEFAULT 0"))


ensure_session_schema()


def ensure_message_schema() -> None:
    inspector = inspect(engine)
    if not inspector.has_table("messages"):
        return

    message_columns = {column["name"] for column in inspector.get_columns("messages")}
    if "consecutive_stuck" not in message_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE messages ADD COLUMN consecutive_stuck INTEGER DEFAULT 0"))


ensure_message_schema()


app = FastAPI(title="Socra AI Reasoning Coach API", version ="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "https://localhost:5173","https://socra-ochre.vercel.app"],
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
    
    session, messages = get_session_with_messages(id, db, lock=True)

    if not session:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Session not found"

        )
    print("\n--- NEW REQUEST RECEIVED ---")
    
    print("1. Calling Progress Evaluator...")
    progress_score = evaluate_progress(
        problem_text = session.problem_text,
        messages=messages,
        student_response = request.content
    )

    
    store_message(
        session_id = id,
        sender = "student",
        content = request.content,
        hint_level = None,
        progress_score = progress_score, 
        db=db
    )

    
    if progress_score == 0:
        session.consecutive_stuck = (session.consecutive_stuck or 0) + 1
        if session.consecutive_stuck >= 2:
            session.current_hint_level = min(session.current_hint_level + 1, 5)
            session.consecutive_stuck = 0
    else:
        session.consecutive_stuck = 0

    db.commit()
    _, updated_messages = get_session_with_messages(id, db)

    print(f"2. Evaluator finished. Score: {progress_score}. Calling Strategy Engine...")
    socra_response = get_next_response(
        problem_text = session.problem_text,
        messages= updated_messages,
        hint_level = session.current_hint_level
    )

    store_message(
        session_id = id,
        sender = "coach",
        content = socra_response,
        hint_level = session.current_hint_level,
        progress_score = None,
        db = db
    )

    print("3. Strategy Engine finished! Returning response to frontend.")

    return{
        "role":"coach",
        "content":socra_response,
        "hint_level": session.current_hint_level,
        "session_status": session.status

    }




     
