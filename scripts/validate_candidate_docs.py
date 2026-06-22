"""Validate candidate-facing assignment documentation."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ARTIFACT_FILES = [
    "artifacts/index.html",
    "artifacts/CANDIDATE_RUNBOOK.html",
    "artifacts/HEALTH_MODEL_GUIDE.html",
    "artifacts/EVIDENCE_AND_VALIDATION_GUIDE.html",
]

CANDIDATE_FILES = [
    "README.md",
    "index.html",
    *ARTIFACT_FILES,
    "SUBMISSION_TEMPLATE.md",
    "SUBMISSION.md",
    "AI_USAGE.md",
    "INCIDENT_NOTE.md",
    "DEFENSE_NOTES.md",
    "docs/ARCHITECTURE.md",
    "docs/OPERATIONS.md",
]

RETIRED_ROOT_HTML = [
    "CANDIDATE_RUNBOOK.html",
    "HEALTH_MODEL_GUIDE.html",
    "EVIDENCE_AND_VALIDATION_GUIDE.html",
]

DEVL_URLS = [
    "https://www.devl.dev/c/timelines/changelog",
    "https://www.devl.dev/c/tours/checklist",
    "https://www.devl.dev/c/layouts/focus-mode",
    "https://www.devl.dev/c/tables/issues",
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
    "artifacts/index.html",
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

REQUIRED_ARTIFACT_PHRASES = {
    "artifacts/index.html": [
        "Market Data Freshness",
        "Start Here",
        "Build",
        "Prove",
        "Do Not Overbuild",
        "Review Gates",
        "make setup",
        "make test",
        "make smoke",
        "safe-to-serve eligibility",
        "GitHub Actions",
    ],
    "artifacts/CANDIDATE_RUNBOOK.html": [
        "Clone and install",
        "Run the baseline",
        "Trigger stale bravo",
        "Recover bravo",
        "Document the health model",
        "Run final validation",
    ],
    "artifacts/HEALTH_MODEL_GUIDE.html": [
        "What We Are Testing",
        "What We Are Not Testing",
        "Health Model",
        "Fail-Closed Reasoning",
        "Follow-Up Interview Prep",
        "safe_to_serve",
    ],
    "artifacts/EVIDENCE_AND_VALIDATION_GUIDE.html": [
        "SRE-001",
        "SRE-010",
        "Hard gate",
        "Scored depth",
        "Candidate fills",
    ],
}


class LinkParser(HTMLParser):
    """Collect local href values from HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for name, value in attrs:
            if name == "href" and value:
                self.hrefs.append(value)


def read_text(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        raise AssertionError(f"missing required candidate file: {relative_path}")
    return path.read_text(encoding="utf-8")


def check_required_paths() -> list[str]:
    errors: list[str] = []
    for relative_path in CANDIDATE_FILES + ["artifacts/COMPONENT_PROVENANCE.md"]:
        if not (ROOT / relative_path).exists():
            errors.append(f"missing required file: {relative_path}")
    for relative_path in RETIRED_ROOT_HTML:
        if (ROOT / relative_path).exists():
            errors.append(f"retired root HTML file still exists: {relative_path}")
    return errors


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
    for relative_path in CANDIDATE_FILES + ["artifacts/COMPONENT_PROVENANCE.md"]:
        text = read_text(relative_path)
        for line_number, line in enumerate(text.splitlines(), start=1):
            if len(line) > 120:
                errors.append(
                    f"{relative_path}:{line_number}: line has {len(line)} chars"
                )
    return errors


def check_artifact_links() -> list[str]:
    errors: list[str] = []
    for relative_path in ["index.html", *ARTIFACT_FILES]:
        parser = LinkParser()
        parser.feed(read_text(relative_path))
        base = (ROOT / relative_path).parent
        for href in parser.hrefs:
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target = href.split("#", 1)[0]
            if not target:
                continue
            if not (base / target).resolve().exists():
                errors.append(f"{relative_path}: broken local link: {href}")
    return errors


def check_provenance() -> list[str]:
    text = read_text("artifacts/COMPONENT_PROVENANCE.md")
    return [
        f"artifacts/COMPONENT_PROVENANCE.md: missing devl URL: {url}"
        for url in DEVL_URLS
        if url not in text
    ]


def main() -> int:
    errors = []
    errors.extend(check_required_paths())
    errors.extend(check_forbidden_phrases())
    errors.extend(check_required_phrases("README.md", REQUIRED_README_PHRASES))
    for relative_path, phrases in REQUIRED_ARTIFACT_PHRASES.items():
        errors.extend(check_required_phrases(relative_path, phrases))
    errors.extend(check_line_lengths())
    errors.extend(check_artifact_links())
    errors.extend(check_provenance())

    if errors:
        print("candidate documentation validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print("candidate documentation validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
