from sqlalchemy.orm import Session
import models

def get_session_with_messages(session_id, db: Session):
    session = db.query(models.Session).filter(
        models.Session.id == session_id
    ).first()

    if not session:
        return None, None
    
    messages = db.query(models.Message).filter(
        models.Message.session_id == session_id
    ).order_by(models.Message.created_at).all()

    return session, messages


def store_message(session_id, sender, content, hint_level, progress_score, db: Session):
    message = models.Message(
        session_id = session_id,
        sender = sender,
        content = content,
        hint_level_at_time = hint_level,
        progress_score = progress_score
    )

    db.add(message)
    db.commit()
    db.refresh(message)
    return message