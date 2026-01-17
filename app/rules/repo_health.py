from app.schemas import CheckResult, Issue
from app.config import WEIGHTS, GITHUB_API

async def run(owner, repo, gc) -> CheckResult:
    commits = await gc.get_commits(owner, repo)

    if len(commits) < 3:
        return CheckResult(score=WEIGHTS["repo_health"] - 5, issues=[Issue(severity="low", message="Low commit activity")])

    return CheckResult(score=WEIGHTS["repo_health"], issues=[])
