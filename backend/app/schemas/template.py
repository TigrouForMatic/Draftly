from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.template import TemplateCategory

class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: TemplateCategory
    template_content: str
    variables_schema: Optional[Dict[str, Any]] = None
    is_public: bool = False
    is_active: bool = True

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[TemplateCategory] = None
    template_content: Optional[str] = None
    variables_schema: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    is_active: Optional[bool] = None

class TemplateInDBBase(TemplateBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Template(TemplateInDBBase):
    pass

class TemplateWithUsage(Template):
    usage_count: int = 0 