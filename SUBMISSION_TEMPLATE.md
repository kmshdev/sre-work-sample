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
Python 3.11+
<other tool and version list>
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

Docs check:

```sh
make docs-check
```

Expected or captured output:

```text
<output>
```

CI minimum: link to a GitHub Actions run, or equivalent CI evidence, that
installs the project and runs tests, smoke, and docs validation.

## 3. Minimum implementation scope

Confirm your submission includes at least:

- A local Python 3.11+ implementation that runs from a fresh checkout.
- A CLI or equivalent workflow for healthy, stale, unknown, and recovered states.
- Automated tests for healthy, stale `bravo`, unknown `bravo`, and recovered `bravo`.
- Smoke evidence for fail-closed stale data, fail-closed unknown data, partial
  availability, and recovery.
- CI evidence that runs install or setup, tests, smoke, and docs validation.
- Architecture and operations notes that match the implemented behavior.

## 4. Health model

Show how the system separates process liveness from safe-to-serve eligibility.

| Feed | Alive signal | Freshness signal | Allowed actions | Blocked actions | Recovery path |
| --- | --- | --- | --- | --- | --- |
| alpha | | | | | |
| bravo | | | | | |
| charlie | | | | | |

Expected-state contract:

| State | Expected result | Evidence |
| --- | --- | --- |
| Healthy feeds | `freshness_status=fresh`, `safe_to_serve=true` | |
| Stale `bravo` | `freshness_status=stale`, `safe_to_serve=false` | |
| Unknown `bravo` tick age | `freshness_status=unknown`, `safe_to_serve=false` | |
| Partial availability | `alpha` and `charlie` stay eligible while `bravo` is unsafe | |
| Recovered `bravo` | `overall_status=eligible` | |

Canonical unsafe actions: `price_order`, `publish_signal`, and
`rebalance_position`.

## 5. Stale-feed scenario

Show the full scenario evidence:

- Trigger command or action.
- Detection signal.
- State transition.
- What becomes blocked.
- What remains allowed.
- Alert, ticket, annotation, or incident path.
- Recovery command or action.
- Evidence that proves recovery worked.

## 6. Unknown tick-age scenario

Show evidence for:

- Trigger command, such as:
  `python -m sre_work_sample.cli scenario unknown --feed bravo --output /tmp/bravo-unknown.json`.
- `freshness_status=unknown`.
- `safe_to_serve=false`.
- Blocked unsafe actions.
- Operator-readable blocked reason.
- Continued eligibility for unaffected feeds.

## 7. GitHub Actions evidence

Link to or paste evidence for the workflow that runs setup, tests, smoke, and
candidate documentation validation.

## 8. Observability and alerting

Document:

- Freshness service-level indicator.
- Liveness or availability service-level indicator.
- Page-worthy stale-data alert.
- Non-page warning or ticket threshold.
- Structured logs, metrics, JSON output, or equivalent evidence from a short run.

## 9. Bad configuration and rollback note

Describe one bad configuration or rollout-safety scenario. Include:

- How detection works.
- How blast radius stays limited.
- Rollback command or decision.
- Evidence that would prove rollback worked.

## 10. Incident note

Link to `INCIDENT_NOTE.md` or include the incident response here. Cover severity,
first five checks, block/allow decision, notifications, operator-facing status,
first runbook action, and closure evidence.

## 11. Security and operator controls

Describe:

- Actions that need audit logs.
- Actions that need confirmation or review.
- Secret and external account handling assumptions.
- Operations that should never be allowed from an unaudited client.

## 12. AI usage

Link to `AI_USAGE.md`, or state that you didn't use AI tools.

If you used AI tools, include:

- Tool names.
- Prompts or task descriptions.
- Generated changes you accepted, edited, or rejected.
- One wrong or incomplete generated result and how you caught it.
- Verification you ran yourself.

## 13. Senior evaluation dimensions

Use this section to point reviewers to your strongest evidence for:

- Reliability model.
- Incident response.
- Automation, CI/CD, and recovery.
- Observability and actionability.
- Tradeoffs and restraint.

## 14. Tradeoffs and follow-up discussion

List what you intentionally didn't build and why. Include the next changes you
would make with more time and the production risks you would discuss in the
follow-up interview.
