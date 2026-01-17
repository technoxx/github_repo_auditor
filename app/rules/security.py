import os
import re
from app.schemas import CheckResult, Issue
from app.config import WEIGHTS, SOURCE_EXTENSIONS

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"api[_-]?key\\s*=\\s*['\"][^'\"]+['\"]", re.I),
    re.compile(r"password\\s*=\\s*['\"][^'\"]+['\"]", re.I),
]

async def run(tree, owner, repo, gc) -> CheckResult:
    for f in tree:
        if f["type"] == "blob" and os.path.splitext(f["path"])[1] in SOURCE_EXTENSIONS:
            content = await gc.get_file_content(owner, repo, f["path"])
            for p in SECRET_PATTERNS:
                if p.search(content):
                    return CheckResult(score=0, issues=[Issue(severity="high", message=f"Secret found in {f['path']}")])

    return CheckResult(score=WEIGHTS["security"], issues=[])