from fastapi import FastAPI, HTTPException, Depends
import httpx
from contextlib import asynccontextmanager
from app.scoring import total_score, calculate_grade
from app.schemas import AuditResponse
from app.github_client import GithubClient
from app.rules import documentation, code_quality, testing, dependencies, security, repo_health


# --- Lifespan for startup/shutdown ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=10.0)
    try:
        yield
    finally:
        await app.state.http_client.aclose()

app = FastAPI(title="GitHub Repository Auditor", lifespan=lifespan)


def get_github_client() -> GithubClient:
    return GithubClient(app.state.http_client)

@app.get("/audit", response_model=AuditResponse)
async def audit(owner: str, repo: str, gc: GithubClient = Depends(get_github_client)):
    tree = await gc.get_tree(owner, repo)
    if not tree:
        raise HTTPException(status_code=400, detail="Empty repository")

    checks = {
        "documentation": await documentation.run(tree, owner, repo, gc),
        "code_quality": await code_quality.run(tree, owner, repo, gc),
        "testing": await testing.run(tree),
        "dependencies": await dependencies.run(tree),
        "security": await security.run(tree, owner, repo, gc),
        "repo_health": await repo_health.run(owner, repo, gc),
    }

    score = total_score(checks)
    grade, passed = calculate_grade(score)

    suggestions = [f"Improve {k.replace('_', ' ')}" for k, v in checks.items() if v.issues]

    return AuditResponse(
        repo=f"{owner}/{repo}",
        score=score,
        grade=grade,
        passed=passed,
        checks=checks,
        suggestions=suggestions,
    )