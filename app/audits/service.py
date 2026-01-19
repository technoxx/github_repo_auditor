from sqlalchemy.orm import Session
from app.db.models import Audit

def save_audit(
    db: Session,
    user_id: int,
    repo: str,
    score: int,
    grade: str,
    result: dict
):
    audit = Audit(
        user_id=user_id,
        repo=repo,
        score=score,
        grade=grade,
        result=result
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


def get_user_audits(db: Session, user_id: int):
    return (
        db.query(Audit)
        .filter(Audit.user_id == user_id)
        .order_by(Audit.created_at.desc())
        .all()
    )