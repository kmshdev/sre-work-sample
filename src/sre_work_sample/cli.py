"""Command-line entry points for the SRE work sample starter."""

from __future__ import annotations

import argparse
import json

from sre_work_sample.runtime_fleet import build_starter_fleet


def run_smoke() -> int:
    """Print starter fleet health in a shape candidates can extend."""
    fleet = build_starter_fleet()
    payload = {
        "control_surface": "starter-cli",
        "runtimes": [runtime.to_dict() for runtime in fleet.runtimes],
        "dependency": fleet.dependency.to_dict(),
        "next_steps": [
            "replace sample health with implemented checks",
            "add two failure scenario triggers",
            "record expected output in SUBMISSION.md",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def main() -> int:
    """Run the requested starter command."""
    parser = argparse.ArgumentParser(prog="sre-work-sample")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("smoke", help="print starter runtime health payload")
    args = parser.parse_args()

    if args.command == "smoke":
        return run_smoke()

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
