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
    "NO_AGENT_INCIDENT.md",
    "DEFENSE_NOTES.md",
    "docs/ARCHITECTURE.md",
    "docs/OPERATIONS.md",
]

FORBIDDEN_PHRASES = [
    "pattern from",
    "pattern",
    "supplied shadcn",
    "registry components",
    "linked pr context",
    "merge readiness translated",
    "issues table",
    "pull-request timeline",
    "inline thread",
    "submission-report.md",
    ">p0<",
    ">p1<",
    ">p2<",
    "trading",
    "broker",
    "exchange",
    "release-safety scenario may count",
    "release-safety evidence or release-safety plan",
    "probably",
    "not just command names",
]

REQUIRED_README_PHRASES = [
    "Table of contents",
    "fresh checkout",
    "three simulated runtimes",
    "mock external dependency",
    "pause or block",
    "two operational failure scenarios",
    "bad rollout or bad configuration",
    "NO_AGENT_INCIDENT.md",
    "AI_USAGE.md",
    "DEFENSE_NOTES.md",
    "The assignment files have one job each",
]

REQUIRED_INDEX_PHRASES = [
    "Build the smallest local runtime-fleet slice",
    "A submission is reviewable when every gate is green",
    "Fresh checkout run path",
    "Smoke command",
    "Delivery automation path",
    "Two operational failure scenarios",
    "Release-safety scenario",
    "Invite <code>kmshdev</code>",
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
            if phrase in lowered:
                errors.append(f"{relative_path}: remove internal phrase: {phrase}")
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
