import os, re


GITHUB_API = "https://api.github.com/repos"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github+json",
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

WEIGHTS = {
    "documentation": 20,
    "code_quality": 25,
    "testing": 15,
    "dependencies": 10,
    "security": 20,
    "repo_health": 10,
}

README_REGEX = re.compile(r"^readme(\\.(md|rst|txt))?$", re.IGNORECASE)
SOURCE_EXTENSIONS = {".py", ".js", ".ts"}
DEPENDENCY_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "poetry.lock",
    "package.json",
    "package-lock.json",
    "yarn.lock",
}
