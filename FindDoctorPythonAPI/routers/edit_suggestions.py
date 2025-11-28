from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import EditSuggestion
from schemas import EditSuggestionCreate, EditSuggestionResponse

router = APIRouter(prefix="/edit-suggestions", tags=["Edit Suggestions"])

@router.post("/", response_model=EditSuggestionResponse, status_code=201)
def create_edit_suggestion(
    suggestion: EditSuggestionCreate,
    db: Session = Depends(get_db)
):
    """Cria uma nova sugestão de edição"""
    db_suggestion = EditSuggestion(**suggestion.model_dump())
    db.add(db_suggestion)
    db.commit()
    db.refresh(db_suggestion)
    return db_suggestion

@router.get("/", response_model=List[EditSuggestionResponse])
def list_edit_suggestions(
    status: str = Query(None, description="Filtrar por status: pending, approved, rejected"),
    establishment_id: str = Query(None, description="Filtrar por CNES do estabelecimento"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todas as sugestões de edição com filtros opcionais"""
    query = db.query(EditSuggestion)
    
    if status:
        query = query.filter(EditSuggestion.status == status)
    if establishment_id:
        query = query.filter(EditSuggestion.establishment_id == establishment_id)
    
    suggestions = query.order_by(EditSuggestion.submitted_at.desc()).offset(skip).limit(limit).all()
    return suggestions

@router.get("/{suggestion_id}", response_model=EditSuggestionResponse)
def get_edit_suggestion(
    suggestion_id: int,
    db: Session = Depends(get_db)
):
    """Busca uma sugestão de edição por ID"""
    suggestion = db.query(EditSuggestion).filter(EditSuggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Sugestão não encontrada")
    return suggestion

@router.delete("/{suggestion_id}", status_code=204)
def delete_edit_suggestion(
    suggestion_id: int,
    db: Session = Depends(get_db)
):
    """Deleta uma sugestão de edição"""
    suggestion = db.query(EditSuggestion).filter(EditSuggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Sugestão não encontrada")
    
    db.delete(suggestion)
    db.commit()
    return None

@router.patch("/{suggestion_id}/status", response_model=EditSuggestionResponse)
def update_suggestion_status(
    suggestion_id: int,
    status: str = Query(..., description="Novo status: approved ou rejected"),
    db: Session = Depends(get_db)
):
    """Atualiza o status de uma sugestão (aprovar ou rejeitar)"""
    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Status inválido. Use 'approved' ou 'rejected'")
    
    suggestion = db.query(EditSuggestion).filter(EditSuggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Sugestão não encontrada")
    
    suggestion.status = status
    db.commit()
    db.refresh(suggestion)
    return suggestion
