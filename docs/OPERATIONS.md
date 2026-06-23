# Operations Notes

Use this file for runbooks, alert notes, rollout decisions, and recovery
procedures.

The reviewer should learn what an operator sees, what they do next, and which
commands prove the system recovered. Keep commands concrete enough to run from a
fresh checkout.

## Fresh-checkout commands

List setup, test, smoke, stale-feed, unknown-data, and recovery commands with
expected output.

Minimum runtime requirement: Python 3.11+. CI should run the same core checks:
setup or install, tests, smoke, and candidate documentation validation.

Minimum implementation scope:

- Local setup and validation commands work from a fresh checkout.
- Operators can inspect healthy, stale, unknown, and recovered states.
- Stale and unknown data fail closed for unsafe actions.
- Fresh unaffected feeds remain eligible during a `bravo` failure.
- Recovery is a rerunnable command or workflow with clear evidence.
- CI/CD evidence covers setup or install, tests, smoke, and docs validation.
- Runbooks and alerts describe only behavior the local evidence exercises.

Starter path:

```sh
make setup
make test
make smoke
.venv/bin/python -m sre_work_sample.cli scenario stale \
  --feed bravo \
  --output /tmp/bravo-stale.json
.venv/bin/python -m sre_work_sample.cli status --state /tmp/bravo-stale.json
.venv/bin/python -m sre_work_sample.cli scenario unknown \
  --feed bravo \
  --output /tmp/bravo-unknown.json
.venv/bin/python -m sre_work_sample.cli status --state /tmp/bravo-unknown.json
.venv/bin/python -m sre_work_sample.cli recover \
  --feed bravo \
  --state /tmp/bravo-stale.json \
  --output /tmp/bravo-recovered.json
```

## Stale-feed scenario

For the implemented stale-feed scenario, include:

- Trigger command.
- Detection signal.
- State transition.
- Blocked unsafe actions.
- Actions that remain allowed.
- Recovery command.
- Evidence location.

## Unknown tick-age scenario

For the implemented unknown-data scenario, include:

- Trigger command.
- Detection signal with `freshness_status=unknown`.
- `safe_to_serve=false`.
- Blocked unsafe actions: `price_order`, `publish_signal`, and
  `rebalance_position`.
- Operator-readable blocked reason.
- Confirmation that `alpha` and `charlie` remain eligible.
- Recovery command or operator decision.
- Evidence location.

Expected-state contract:

| State | Operational expectation |
| --- | --- |
| Healthy feeds | No unsafe feeds and no blocked reason. |
| Stale `bravo` | Unsafe actions blocked because tick age exceeds threshold. |
| Unknown `bravo` tick age | Unsafe actions blocked because tick age is missing. |
| Partial availability | Operators can continue safe work for unaffected feeds. |
| Recovered `bravo` | Eligibility restored and incident can close with evidence. |

## Bad configuration and rollback

Describe one bad configuration or rollout-safety scenario. Keep it scoped to the
freshness service. Include detection, blast radius, rollback decision, and
evidence that would prove rollback worked.

## Alerts and operator actions

For each alert, include threshold, severity, owner, and first action.

At minimum, include:

- A page-worthy stale-data alert.
- A non-page warning or ticket threshold.

Reviewer focus areas are reliability model, incident response, automation,
CI/CD and recovery, observability and actionability, and tradeoffs and
restraint.

Don't include alerts that your local evidence never exercises.
