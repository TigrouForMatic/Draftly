from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.user import User, UserUpdate
from app.models.user import User as UserModel
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Récupère la liste des utilisateurs (admin seulement)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé"
        )
    
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/profile", response_model=User)
async def get_user_profile(
    current_user: UserModel = Depends(get_current_user)
):
    """Récupère le profil de l'utilisateur connecté"""
    return current_user

@router.put("/profile", response_model=User)
async def update_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Met à jour le profil de l'utilisateur connecté"""
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user 