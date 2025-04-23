from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import datetime
import uuid

class DocumentBase(BaseModel):
    """Base model for document data."""
    content: str
    title: str
    url: Optional[str] = None
    summary: Optional[str] = None
    metadata: Dict[str, any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    category: Optional[str] = None

class DocumentCreate(DocumentBase):
    """Model for creating a new document."""
    author: Optional[str] = None
    date: Optional[str] = Field(
        default_factory=lambda: datetime.datetime.now().isoformat()
    )

class DocumentUpdate(BaseModel):
    """Model for updating an existing document."""
    content: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    metadata: Optional[Dict[str, any]] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None

class Document(DocumentBase):
    """Model for a document in the system."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    embedding: List[float]
    version: int = 1
    author: Optional[str] = None
    date: str = Field(
        default_factory=lambda: datetime.datetime.now().isoformat()
    )

    class Config:
        orm_mode = True
