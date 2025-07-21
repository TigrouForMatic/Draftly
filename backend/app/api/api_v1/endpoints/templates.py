from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.template import Template, TemplateCreate, TemplateUpdate, TemplateWithUsage
from app.models.template import Template as TemplateModel
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[TemplateWithUsage])
async def get_templates(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    public_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère la liste des templates"""
    query = db.query(TemplateModel)
    
    if public_only:
        query = query.filter(TemplateModel.is_public == True)
    else:
        # Templates publics + templates de l'utilisateur
        query = query.filter(
            (TemplateModel.is_public == True) | 
            (TemplateModel.user_id == current_user.id)
        )
    
    if category:
        query = query.filter(TemplateModel.category == category)
    
    templates = query.offset(skip).limit(limit).all()
    return templates

@router.post("/", response_model=Template)
async def create_template(
    template: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée un nouveau template"""
    db_template = TemplateModel(
        **template.dict(),
        user_id=current_user.id
    )
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.get("/{template_id}", response_model=Template)
async def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère un template spécifique"""
    template = db.query(TemplateModel).filter(
        TemplateModel.id == template_id,
        (TemplateModel.is_public == True) | 
        (TemplateModel.user_id == current_user.id)
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template non trouvé"
        )
    
    return template

@router.put("/{template_id}", response_model=Template)
async def update_template(
    template_id: int,
    template_update: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Met à jour un template"""
    db_template = db.query(TemplateModel).filter(
        TemplateModel.id == template_id,
        TemplateModel.user_id == current_user.id
    ).first()
    
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template non trouvé"
        )
    
    for field, value in template_update.dict(exclude_unset=True).items():
        setattr(db_template, field, value)
    
    db.commit()
    db.refresh(db_template)
    return db_template

@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime un template"""
    template = db.query(TemplateModel).filter(
        TemplateModel.id == template_id,
        TemplateModel.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template non trouvé"
        )
    
    db.delete(template)
    db.commit()
    return {"message": "Template supprimé avec succès"}

@router.get("/categories/list")
async def get_template_categories():
    """Récupère la liste des catégories de templates"""
    from app.models.template import TemplateCategory
    return [category.value for category in TemplateCategory]

@router.post("/{template_id}/duplicate", response_model=Template)
async def duplicate_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Duplique un template"""
    original_template = db.query(TemplateModel).filter(
        TemplateModel.id == template_id,
        (TemplateModel.is_public == True) | 
        (TemplateModel.user_id == current_user.id)
    ).first()
    
    if not original_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template non trouvé"
        )
    
    # Créer une copie
    new_template = TemplateModel(
        name=f"{original_template.name} (copie)",
        description=original_template.description,
        category=original_template.category,
        template_content=original_template.template_content,
        variables_schema=original_template.variables_schema,
        is_public=False,  # La copie est privée
        is_active=True,
        user_id=current_user.id
    )
    
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template 