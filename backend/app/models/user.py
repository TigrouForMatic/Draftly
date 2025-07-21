from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Null si Auth0
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Relations
    documents = relationship("Document", back_populates="user")
    templates = relationship("Template", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email}>" 