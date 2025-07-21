from typing import List, Union
from pydantic import AnyHttpUrl, BaseSettings, validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Draftly"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # FastAPI dev server
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Base de données
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./draftly.db")
    
    # Sécurité
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Auth0 (optionnel)
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN", "")
    AUTH0_API_AUDIENCE: str = os.getenv("AUTH0_API_AUDIENCE", "")
    AUTH0_ISSUER: str = os.getenv("AUTH0_ISSUER", "")
    
    # Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Templates
    TEMPLATES_DIR: str = "app/templates"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 