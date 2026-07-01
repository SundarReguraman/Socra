from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from database import engine, get_db
import models
import schemas

models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Socra AI Reasoning Coach API", version ="1.0")

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

    first_question = "What is the question asking you to do, break it down into your own words"

    first_message = models.Messages(
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



     
