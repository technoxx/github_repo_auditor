# 🚀 GitHub Repository Auditor

A **production-grade FastAPI backend service** that analyzes public GitHub repositories and generates an **explainable quality score**, detailed findings, and actionable improvement suggestions based on documentation, code quality, security hygiene, testing practices, and repository health.

Designed as a **real-world backend system**, not a toy project.

---

## ✨ Key Features

### 🔍 Repository Analysis
- Analyzes **public GitHub repositories** using `owner/repo`
- Full repository traversal using **GitHub Tree API**
- Supports **nested folder structures** and arbitrary layouts
- Correctly handles **case-sensitive file paths**

---

### 📄 Documentation Evaluation
- Detects README files regardless of:
  - Filename casing (`README`, `readme`, etc.)
  - Format (`.md`, `.rst`, `.txt`)
- Validates README quality:
  - Non-empty, meaningful content
  - Presence of usage examples
  - Correct placement at repository root
- Flags missing or weak documentation

---

### 🧠 Code Quality & Structure
- Detects source code across entire repository
- Supports **Python, JavaScript, and TypeScript**
- Identifies structured project layouts (`src/`, `app/`, `backend/`, etc.)
- Avoids false positives from empty or placeholder files

---

### 🧪 Testing Practices
- Detects test files and test directories
- Supports common naming conventions (`test_*.py`, `*.spec.js`, etc.)
- Flags repositories with **missing or insufficient tests**

---

### 📦 Dependency & Build Hygiene
- Detects dependency manifests and lock files
- Ensures dependencies are explicitly defined
- Flags repositories without proper dependency management

---

### 🔐 Security Hygiene (High Severity)
- Scans source code for **hardcoded secrets**
- Detects common credential patterns:
  - API keys
  - Tokens
  - Passwords
- Security violations significantly impact score

---

### 📊 Repository Health
- Analyzes **commit history depth**
- Flags extremely low or trivial commit activity
- Rewards consistent, meaningful commit history

---

## 🧮 Scoring & Evaluation

- Generates a **weighted quality score (0–100)**
- Assigns a **grade** (A / B / C / D / F)
- Provides **pass/fail** evaluation
- Detailed breakdown of each audit category
- Scores are **consistent, explainable, and transparent**


---

## 📤 Output Format

Audit results are returned as **structured JSON**:

```json
{
  "score": 82,
  "grade": "B",
  "pass": true,
  "issues": [
    "Missing tests directory",
    "README lacks usage examples"
  ],
  "suggestions": [
    "Add unit tests for core modules",
    "Include usage examples in README"
  ],
  "checks": {
    "documentation": 15,
    "code_quality": 25,
    "security": 20,
    "testing": 10,
    "repository_health": 12
  }
}

```

## 📌 Future Enhancements (Currently Working)


- **JWT-based authentication & Rate Limiting:** Secure password hashing (bcrypt) and protected audit endpoints
- **Per-user rate limiting:** on expensive operations and prevents abuse and controls GitHub API usage
* **Redis-backed distributed rate limiting:** Transitioning from in-memory to Redis to support multi-worker deployments.
* **Alembic migrations:** Implementing structured database versioning and schema evolution.
* **Unit & integration tests:** Comprehensive test suite using `pytest` and `httpx` for async API testing.
* **Web dashboard for audit visualization:** A frontend interface to track, filter, and visualize security audit results.
