from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.document import Document, DocumentCreate, DocumentUpdate, DocumentWithTemplate
from app.models.document import Document as DocumentModel
from app.services.ai_service import AIService
from app.services.document_service import DocumentService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()
ai_service = AIService()
document_service = DocumentService()

@router.get("/", response_model=List[DocumentWithTemplate])
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    document_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère la liste des documents de l'utilisateur"""
    query = db.query(DocumentModel).filter(DocumentModel.user_id == current_user.id)
    
    if document_type:
        query = query.filter(DocumentModel.document_type == document_type)
    
    documents = query.offset(skip).limit(limit).all()
    return documents

@router.post("/", response_model=Document)
async def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée un nouveau document"""
    db_document = DocumentModel(
        **document.dict(),
        user_id=current_user.id
    )
    
    # Si des données de template sont fournies, générer le contenu
    if document.template_data:
        try:
            # Utiliser l'IA pour générer le contenu
            content = await ai_service.generate_document_content(
                template_content="",  # À adapter selon le template
                template_data=document.template_data,
                document_type=document.document_type.value
            )
            db_document.content = content
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur lors de la génération du contenu: {str(e)}"
            )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@router.get("/{document_id}", response_model=DocumentWithTemplate)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère un document spécifique"""
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    return document

@router.put("/{document_id}", response_model=Document)
async def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Met à jour un document"""
    db_document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.user_id == current_user.id
    ).first()
    
    if not db_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    for field, value in document_update.dict(exclude_unset=True).items():
        setattr(db_document, field, value)
    
    db.commit()
    db.refresh(db_document)
    return db_document

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime un document"""
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    db.delete(document)
    db.commit()
    return {"message": "Document supprimé avec succès"}

@router.post("/{document_id}/generate")
async def generate_document_content(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Génère le contenu d'un document avec l'IA"""
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    if not document.template_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucune donnée de template fournie"
        )
    
    try:
        content = await ai_service.generate_document_content(
            template_content="",  # À adapter selon le template
            template_data=document.template_data,
            document_type=document.document_type.value
        )
        
        document.content = content
        db.commit()
        db.refresh(document)
        
        return {"content": content}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération: {str(e)}"
        )

@router.post("/{document_id}/export")
async def export_document(
    document_id: int,
    format: str = "docx",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Exporte un document en DOCX ou PDF"""
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    if not document.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le document n'a pas de contenu à exporter"
        )
    
    try:
        filename = f"document_{document_id}"
        
        if format == "docx":
            file_path = document_service.create_docx(
                content=document.content,
                filename=filename
            )
        elif format == "pdf":
            docx_path = document_service.create_docx(
                content=document.content,
                filename=filename
            )
            file_path = document_service.create_pdf_from_docx(docx_path)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Format non supporté. Utilisez 'docx' ou 'pdf'"
            )
        
        # Mettre à jour le chemin du fichier dans la base
        document.file_path = file_path
        db.commit()
        
        return {"file_path": file_path, "message": f"Document exporté en {format.upper()}"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'export: {str(e)}"
        ) 