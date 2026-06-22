# Candidate Submission Template

Use this template for `SUBMISSION.md`. Link to commands, logs, screenshots,
workflow runs, or files when evidence is clearer than prose.

## 1. Summary

State what you changed in 5-8 sentences. Include the stack, freshness behavior,
main reliability idea, and what a reviewer should run first.

## 2. Fresh-checkout setup and run commands

Assume the reviewer cloned the repository on a new machine.

Prerequisites and supported versions:

```text
<tool and version list>
```

Setup commands:

```sh
make setup
```

Test command:

```sh
make test
```

Smoke command:

```sh
make smoke
```

Expected or captured output:

```text
<output>
```

## 3. Health model

Show how the system separates process liveness from safe-to-serve eligibility.

| Feed | Alive signal | Freshness signal | Allowed actions | Blocked actions | Recovery path |
| --- | --- | --- | --- | --- | --- |
| alpha | | | | | |
| bravo | | | | | |
| charlie | | | | | |

## 4. Stale-feed scenario

Show the full scenario evidence:

- Trigger command or action.
- Detection signal.
- State transition.
- What becomes blocked.
- What remains allowed.
- Alert, ticket, annotation, or incident path.
- Recovery command or action.
- Evidence that proves recovery worked.

## 5. GitHub Actions evidence

Link to or paste evidence for the workflow that runs setup, tests, smoke, and
candidate documentation validation.

## 6. Observability and alerting

Document:

- Freshness service-level indicator.
- Liveness or availability service-level indicator.
- Page-worthy stale-data alert.
- Non-page warning or ticket threshold.
- Structured logs, metrics, JSON output, or equivalent evidence from a short run.

## 7. Bad configuration and rollback note

Describe one bad configuration or rollout-safety scenario. Include:

- How detection works.
- How blast radius stays limited.
- Rollback command or decision.
- Evidence that would prove rollback worked.

## 8. Incident note

Link to `INCIDENT_NOTE.md` or include the incident response here. Cover severity,
first five checks, block/allow decision, notifications, operator-facing status,
first runbook action, and closure evidence.

## 9. Security and operator controls

Describe:

- Actions that need audit logs.
- Actions that need confirmation or review.
- Secret and external account handling assumptions.
- Operations that should never be allowed from an unaudited client.

## 10. AI usage

Link to `AI_USAGE.md`, or state that you did not use AI tools.

If you used AI tools, include:

- Tool names.
- Prompts or task descriptions.
- Generated changes you accepted, edited, or rejected.
- One wrong or incomplete generated result and how you caught it.
- Verification you ran yourself.

## 11. Tradeoffs and follow-up defense

List what you intentionally did not build and why. Include the next changes you
would make with more time and the production risks you would discuss in the
follow-up interview.
