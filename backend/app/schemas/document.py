from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.document import DocumentType, DocumentStatus

class DocumentBase(BaseModel):
    title: str
    document_type: DocumentType
    status: DocumentStatus = DocumentStatus.DRAFT

class DocumentCreate(DocumentBase):
    template_data: Optional[Dict[str, Any]] = None
    template_id: Optional[int] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[DocumentStatus] = None
    content: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None

class DocumentInDBBase(DocumentBase):
    id: int
    content: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None
    file_path: Optional[str] = None
    user_id: int
    template_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Document(DocumentInDBBase):
    pass

class DocumentWithTemplate(Document):
    template_name: Optional[str] = None 