from sqlalchemy import Column, String, Text, ForeignKey, JSON, Enum, Integer
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel

class DocumentType(str, enum.Enum):
    DEVIS = "devis"
    FACTURE = "facture"
    CONTRAT = "contrat"
    LETTRE = "lettre"
    CGV = "cgv"
    AUTRE = "autre"

class DocumentStatus(str, enum.Enum):
    DRAFT = "draft"
    FINALIZED = "finalized"
    SENT = "sent"
    ARCHIVED = "archived"

class Document(BaseModel):
    __tablename__ = "documents"
    
    title = Column(String(255), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    content = Column(Text, nullable=True)  # Contenu généré
    template_data = Column(JSON, nullable=True)  # Données du template
    file_path = Column(String(500), nullable=True)  # Chemin vers le fichier généré
    
    # Relations
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="documents")
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    template = relationship("Template", back_populates="documents")
    
    def __repr__(self):
        return f"<Document {self.title}>" 