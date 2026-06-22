"""Validate candidate-facing assignment documentation."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CANDIDATE_FILES = [
    "README.md",
    "index.html",
    "CANDIDATE_RUNBOOK.html",
    "HEALTH_MODEL_GUIDE.html",
    "EVIDENCE_AND_VALIDATION_GUIDE.html",
    "SUBMISSION_TEMPLATE.md",
    "SUBMISSION.md",
    "AI_USAGE.md",
    "INCIDENT_NOTE.md",
    "DEFENSE_NOTES.md",
    "docs/ARCHITECTURE.md",
    "docs/OPERATIONS.md",
]

FORBIDDEN_PHRASES = [
    "critical runtime platform",
    "7 calendar days",
    "20-50",
    "NO_AGENT_INCIDENT.md",
    "no-agent incident",
    "two operational failure scenarios",
    "three simulated runtimes",
    "mock external dependency",
    "release-safety scenario may count",
    "runnable or inspectable",
    "8-12 focused hours",
    ".eval/",
]

REQUIRED_README_PHRASES = [
    "Table of contents",
    "6 calendar days",
    "6-8 focused hours",
    "Market Data Freshness",
    "alpha",
    "bravo",
    "charlie",
    "make setup",
    "make test",
    "make smoke",
    "GitHub Actions",
    "safe-to-serve eligibility",
    "INCIDENT_NOTE.md",
    "AI_USAGE.md",
    "DEFENSE_NOTES.md",
]

REQUIRED_INDEX_PHRASES = [
    "Market Data Freshness",
    "Fresh checkout run path",
    "make setup",
    "make test",
    "make smoke",
    "A submission is reviewable when every gate is green",
]


def read_text(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        raise AssertionError(f"missing required candidate file: {relative_path}")
    return path.read_text(encoding="utf-8")


def check_forbidden_phrases() -> list[str]:
    errors: list[str] = []
    for relative_path in CANDIDATE_FILES:
        text = read_text(relative_path)
        lowered = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"{relative_path}: remove retired phrase: {phrase}")
    return errors


def check_required_phrases(relative_path: str, phrases: list[str]) -> list[str]:
    text = read_text(relative_path)
    return [
        f"{relative_path}: missing required phrase: {phrase}"
        for phrase in phrases
        if phrase not in text
    ]


def check_line_lengths() -> list[str]:
    errors: list[str] = []
    for relative_path in CANDIDATE_FILES:
        text = read_text(relative_path)
        for line_number, line in enumerate(text.splitlines(), start=1):
            if len(line) > 100:
                errors.append(
                    f"{relative_path}:{line_number}: line has {len(line)} chars"
                )
    return errors


def check_links() -> list[str]:
    errors: list[str] = []
    index = read_text("index.html")
    for link in [
        "README.md",
        "CANDIDATE_RUNBOOK.html",
        "HEALTH_MODEL_GUIDE.html",
        "EVIDENCE_AND_VALIDATION_GUIDE.html",
        "SUBMISSION_TEMPLATE.md",
    ]:
        if f'href="{link}"' not in index:
            errors.append(f"index.html: missing link to {link}")
    return errors


def main() -> int:
    errors = []
    errors.extend(check_forbidden_phrases())
    errors.extend(check_required_phrases("README.md", REQUIRED_README_PHRASES))
    errors.extend(check_required_phrases("index.html", REQUIRED_INDEX_PHRASES))
    errors.extend(check_line_lengths())
    errors.extend(check_links())

    if errors:
        print("candidate documentation validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print("candidate documentation validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
