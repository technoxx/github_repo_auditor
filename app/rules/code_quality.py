import os
from app.schemas import CheckResult, Issue
from app.config import WEIGHTS, SOURCE_EXTENSIONS

async def run(tree, owner, repo, gc) -> CheckResult:
    score = WEIGHTS["code_quality"]
    issues = []

    files = [f for f in tree if f["type"] == "blob" and os.path.splitext(f["path"])[1] in SOURCE_EXTENSIONS]

    if not files:
        return CheckResult(score=0, issues=[Issue(severity="high", message="No source code detected")])

    meaningful = 0
    for f in files[:20]:
        content = await gc.get_file_content(owner, repo, f["path"])
        lines = [l for l in content.splitlines() if l.strip() and not l.strip().startswith("#")]
        if len(lines) > 10:
            meaningful += 1

    if meaningful == 0:
        score -= 15
        issues.append(Issue(severity="high", message="Only trivial code found"))

    return CheckResult(score=max(score, 0), issues=issues)
