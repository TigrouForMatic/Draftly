from sqlalchemy import Column, String, Text, ForeignKey, JSON, Boolean, Enum, Integer
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel

class TemplateCategory(str, enum.Enum):
    FREELANCE = "freelance"
    AGENCE = "agence"
    JURIDIQUE = "juridique"
    COMPTABILITE = "comptabilite"
    RH = "rh"
    AUTRE = "autre"

class Template(BaseModel):
    __tablename__ = "templates"
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(TemplateCategory), nullable=False)
    template_content = Column(Text, nullable=False)  # Contenu Jinja2
    variables_schema = Column(JSON, nullable=True)  # Schéma des variables
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Relations
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null pour templates publics
    user = relationship("User", back_populates="templates")
    documents = relationship("Document", back_populates="template")
    
    def __repr__(self):
        return f"<Template {self.name}>" 