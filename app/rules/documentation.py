import os
import re
from app.schemas import CheckResult, Issue
from app.config import WEIGHTS, README_REGEX

async def run(tree, owner, repo, gc) -> CheckResult:
    issues = []
    score = WEIGHTS["documentation"]

    readmes = [f for f in tree if f["type"] == "blob" and README_REGEX.match(os.path.basename(f["path"]))]

    if not readmes:
        return CheckResult(score=0, issues=[Issue(severity="high", message="No README found")])

    root = next((r for r in readmes if "/" not in r["path"]), readmes[0])
    content = await gc.get_file_content(owner, repo, root["path"])

    if len(content.strip()) < 300:
        score -= 10
        issues.append(Issue(severity="medium", message="Weak README content"))

    if not re.search(r"usage|install|example", content, re.IGNORECASE):
        score -= 5
        issues.append(Issue(severity="low", message="No usage examples found"))

    return CheckResult(score=max(score, 0), issues=issues)
