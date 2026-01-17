import os
import re
from app.schemas import CheckResult, Issue
from app.config import WEIGHTS

PATTERNS = [
    re.compile(r"test_.*\\.py"),
    re.compile(r".*_test\\.py"),
    re.compile(r".*\\.(spec|test)\\.(js|ts)"),
]

async def run(tree) -> CheckResult:
    score = WEIGHTS["testing"]

    for f in tree:
        if f["type"] == "blob":
            name = os.path.basename(f["path"])
            if any(p.match(name) for p in PATTERNS) or "tests/" in f["path"]:
                return CheckResult(score=score, issues=[])

    return CheckResult(score=0, issues=[Issue(severity="medium", message="No tests found")])
