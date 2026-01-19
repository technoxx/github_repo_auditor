from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.audits.service import get_user_audits

router = APIRouter(prefix="/audits", tags=["audits"])

@router.get("/me")
def my_audits(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    audits = get_user_audits(db, user.id)
    return [
        {
            "repo": a.repo,
            "score": a.score,
            "grade": a.grade,
            "created_at": a.created_at
        }
        for a in audits
    ]