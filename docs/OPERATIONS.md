# Operations Notes

Use this file for runbooks, alert notes, rollout decisions, and recovery
procedures.

The reviewer should learn what an operator sees, what they do next, and which
commands prove the system recovered. Keep commands concrete enough to run from a
fresh checkout.

## Fresh-checkout commands

List setup, test, smoke, stale-feed, and recovery commands with expected output.

Starter path:

```sh
make setup
make test
make smoke
.venv/bin/python -m sre_work_sample.cli scenario stale \
  --feed bravo \
  --output /tmp/bravo-stale.json
.venv/bin/python -m sre_work_sample.cli status --state /tmp/bravo-stale.json
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

## Bad configuration and rollback

Describe one bad configuration or rollout-safety scenario. Keep it scoped to the
freshness service. Include detection, blast radius, rollback decision, and
evidence that would prove rollback worked.

## Alerts and operator actions

For each alert, include threshold, severity, owner, and first action.

At minimum, include:

- A page-worthy stale-data alert.
- A non-page warning or ticket threshold.

Do not include alerts that your local evidence never exercises.
