from .config import WEIGHTS

def calculate_grade(score: int):
    if score >= 90:
        return "A", True
    if score >= 75:
        return "B", True
    if score >= 60:
        return "C", True
    return "D", False


def total_score(checks: dict) -> int:
    return sum(result.score for result in checks.values())
