from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.schemas import AssignmentCreate, AssignmentOut
from ..models.models import Assignment
from .deps import get_db, get_current_user
from typing import List

router = APIRouter(prefix="/assignments", tags=["assignments"])

@router.post("", response_model=AssignmentOut)
def create_assignment(payload: AssignmentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    assignment = Assignment(**payload.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.get("", response_model=List[AssignmentOut])
def list_assignments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Assignment).order_by(Assignment.created_at.desc()).all()
