import json
import os
import subprocess
import sys
from pathlib import Path


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd() / "src")
    return subprocess.run(
        [sys.executable, "-m", "sre_work_sample.cli", *args],
        check=True,
        capture_output=True,
        env=env,
        text=True,
    )


def test_unknown_scenario_cli_writes_fail_closed_state(tmp_path: Path) -> None:
    output = tmp_path / "bravo-unknown.json"

    scenario = run_cli("scenario", "unknown", "--feed", "bravo", "--output", str(output))
    status = run_cli("status", "--state", str(output))

    scenario_payload = json.loads(scenario.stdout)
    status_payload = json.loads(status.stdout)
    feeds = {feed["name"]: feed for feed in status_payload["feeds"]}

    assert scenario_payload == {
        "feed": "bravo",
        "scenario": "unknown",
        "state": str(output),
    }
    assert status_payload["overall_status"] == "restricted"
    assert status_payload["unsafe_feeds"] == ["bravo"]
    assert feeds["bravo"]["freshness_status"] == "unknown"
    assert not feeds["bravo"]["safe_to_serve"]
    assert feeds["bravo"]["blocked_reason"] == "last tick age is unknown"
