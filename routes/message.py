from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.message import MessageInput
from agents.orchestrator import process_message
from db.database import SessionLocal
from db.models import ConversationMessage
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/message")
def handle_message(data: MessageInput, db: Session = Depends(get_db)):
    result = process_message(data.message)

    record = ConversationMessage(
        conversation_id=str(uuid.uuid4()),
        message_id=str(uuid.uuid4()),
        user_message=data.message,
        topic=result["topic"],
        department=result["department"],
        resolution=result["resolution"],
        confidence=str(result["confidence"])
    )

    db.add(record)
    db.commit()

    return result
