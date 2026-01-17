import os
from app.schemas import CheckResult, Issue
from app.config import WEIGHTS, DEPENDENCY_FILES

async def run(tree) -> CheckResult:
    found = {os.path.basename(f["path"]) for f in tree if f["type"] == "blob"}

    if not (found & DEPENDENCY_FILES):
        return CheckResult(score=0, issues=[Issue(severity="medium", message="No dependency files found")])

    return CheckResult(score=WEIGHTS["dependencies"], issues=[])
