"""Command-line entry points for the SRE work sample starter."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any

from sre_work_sample.freshness import (
    UNSAFE_ACTIONS,
    evaluate_system,
    healthy_state,
    set_feed_age,
    set_feed_age_unknown,
)


def load_state(path: Path | None) -> dict[str, Any]:
    """Load feed state from JSON, or return the built-in healthy state."""
    if path is None:
        return healthy_state()
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_state(path: Path, state: dict[str, Any]) -> None:
    """Write feed state as stable JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")


def print_json(payload: dict[str, Any]) -> None:
    """Print stable JSON for command output and tests."""
    print(json.dumps(payload, indent=2, sort_keys=True))


def command_status(args: argparse.Namespace) -> int:
    """Print feed eligibility status."""
    print_json(evaluate_system(load_state(args.state)))
    return 0


def command_scenario(args: argparse.Namespace) -> int:
    """Write a scenario state file."""
    if args.kind == "stale":
        next_state = set_feed_age(load_state(args.state), args.feed, args.age_seconds)
    elif args.kind == "unknown":
        next_state = set_feed_age_unknown(load_state(args.state), args.feed)
    else:
        raise ValueError(f"unsupported scenario {args.kind!r}")
    write_state(args.output, next_state)
    print_json({"scenario": args.kind, "feed": args.feed, "state": str(args.output)})
    return 0


def command_recover(args: argparse.Namespace) -> int:
    """Write a recovered state file."""
    next_state = set_feed_age(load_state(args.state), args.feed, args.age_seconds)
    write_state(args.output, next_state)
    print_json({"recovered": args.feed, "state": str(args.output)})
    return 0


def command_smoke(_: argparse.Namespace) -> int:
    """Run the starter smoke check."""
    healthy = healthy_state()
    healthy_status = evaluate_system(healthy)
    if healthy_status["overall_status"] != "eligible":
        raise RuntimeError("healthy state is not eligible")

    stale = set_feed_age(healthy, "bravo", 660)
    stale_status = evaluate_system(stale)
    if stale_status["unsafe_feeds"] != ["bravo"]:
        raise RuntimeError("expected only bravo to be unsafe")
    stale_feeds = {feed["name"]: feed for feed in stale_status["feeds"]}
    if not stale_feeds["alpha"]["safe_to_serve"]:
        raise RuntimeError("expected alpha to stay eligible while bravo is stale")
    if not stale_feeds["charlie"]["safe_to_serve"]:
        raise RuntimeError("expected charlie to stay eligible while bravo is stale")

    unknown = set_feed_age_unknown(healthy, "bravo")
    unknown_status = evaluate_system(unknown)
    unknown_feeds = {feed["name"]: feed for feed in unknown_status["feeds"]}
    unknown_bravo = unknown_feeds["bravo"]
    if unknown_status["unsafe_feeds"] != ["bravo"]:
        raise RuntimeError("expected only bravo to be unsafe when tick age is unknown")
    if unknown_bravo["freshness_status"] != "unknown":
        raise RuntimeError("expected unknown bravo freshness status")
    if unknown_bravo["safe_to_serve"]:
        raise RuntimeError("expected unknown bravo to fail closed")
    if unknown_bravo["blocked_actions"] != UNSAFE_ACTIONS:
        raise RuntimeError("expected unsafe actions to be blocked for unknown bravo")
    if not unknown_bravo["blocked_reason"]:
        raise RuntimeError("expected operator-readable blocked reason for unknown bravo")

    recovered = set_feed_age(stale, "bravo", 5)
    recovered_status = evaluate_system(recovered)
    if recovered_status["overall_status"] != "eligible":
        raise RuntimeError("recovered state is not eligible")

    with tempfile.TemporaryDirectory() as directory:
        write_state(Path(directory) / "bravo-recovered.json", recovered)

    print_json(
        {
            "smoke": "passed",
            "checks": [
                "healthy feeds eligible",
                "stale bravo fails closed",
                "unknown data fails closed",
                "alpha and charlie remain eligible",
                "bravo recovery restores eligibility",
            ],
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the command parser."""
    parser = argparse.ArgumentParser(prog="python -m sre_work_sample.cli")
    subcommands = parser.add_subparsers(dest="command", required=True)

    status = subcommands.add_parser("status", help="print feed status")
    status.add_argument("--state", type=Path)
    status.set_defaults(func=command_status)

    scenario = subcommands.add_parser("scenario", help="write a scenario state")
    scenario.add_argument("kind", choices=["stale", "unknown"])
    scenario.add_argument("--feed", required=True, choices=["alpha", "bravo", "charlie"])
    scenario.add_argument("--state", type=Path)
    scenario.add_argument("--output", type=Path, required=True)
    scenario.add_argument("--age-seconds", type=int, default=660)
    scenario.set_defaults(func=command_scenario)

    recover = subcommands.add_parser("recover", help="write a recovered state")
    recover.add_argument("--feed", required=True, choices=["alpha", "bravo", "charlie"])
    recover.add_argument("--state", type=Path, required=True)
    recover.add_argument("--output", type=Path, required=True)
    recover.add_argument("--age-seconds", type=int, default=5)
    recover.set_defaults(func=command_recover)

    smoke = subcommands.add_parser("smoke", help="run starter smoke checks")
    smoke.set_defaults(func=command_smoke)
    return parser


def main() -> int:
    """Run the requested starter command."""
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
