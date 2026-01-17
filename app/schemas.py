from pydantic import BaseModel
from typing import List, Dict

class Issue(BaseModel):
    severity: str
    message: str

class CheckResult(BaseModel):
    score: int
    issues: List[Issue]

class AuditResponse(BaseModel):
    repo: str
    score: int
    grade: str
    passed: bool
    checks: Dict[str, CheckResult]
    suggestions: List[str]
