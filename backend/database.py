from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    func,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text
from typing import List, Optional, Dict, Any
from datetime import datetime
import json


# Database configuration and setup
engine = create_engine("sqlite:///database.db", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Note(Base):
    """
    Enhanced Note model with additional fields for better functionality.

    Fields:
    - id: Primary key
    - user_id: Foreign key to identify the note owner
    - content: The actual note content
    - title: Optional title for the note
    - category: Optional category for organization
    - tags: JSON string of tags for better searchability
    - is_archived: Soft delete flag
    - is_pinned: Flag for important notes
    - created_at: Timestamp when note was created
    - updated_at: Timestamp when note was last modified
    """

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    title = Column(String, nullable=True, index=True)
    category = Column(String, nullable=True, index=True)
    tags = Column(Text, nullable=True)  # JSON string of tags
    is_archived = Column(Boolean, default=False, index=True)
    is_pinned = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True
    )


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class NoteRepository:

    @staticmethod
    def get_notes_by_user(user_id: str) -> List[Note]:
        db = SessionLocal()
        try:
            return db.query(Note).filter(Note.user_id == user_id).all()
        finally:
            db.close()

    @staticmethod
    def create_note(user_id: str, content: str) -> Note:
        db = SessionLocal()
        try:
            note = Note(user_id=user_id, content=content)
            db.add(note)
            db.commit()
            db.refresh(note)
            return note
        finally:
            db.close()
