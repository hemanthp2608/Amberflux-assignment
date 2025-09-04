from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from ..models.models import Submission, Assignment
from ..schemas.schemas import SubmissionOut
from .deps import get_db, get_current_user
from typing import List
import os
from datetime import datetime

router = APIRouter(prefix="/submissions", tags=["submissions"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "backend/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("", response_model=SubmissionOut)
async def create_submission(
    assignment_id: int = Form(...),
    comment: str | None = Form(None),
    upload: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    assignment = db.get(Assignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{user.id}_{assignment_id}_{timestamp}_{upload.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await upload.read())
    sub = Submission(assignment_id=assignment_id, user_id=user.id, file_path=file_path, comment=comment)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

@router.get("/by-assignment/{assignment_id}", response_model=List[SubmissionOut])
def list_by_assignment(assignment_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(Submission).filter(Submission.assignment_id == assignment_id).all()
