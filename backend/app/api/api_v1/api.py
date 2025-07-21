from fastapi import APIRouter
from app.api.api_v1.endpoints import documents, templates, users, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"]) 