# Architecture Notes

Use this file to explain the freshness service you built. The reviewer should
learn what runs locally, where state lives, and which tradeoffs are intentional.

## Explain the local system shape

Cover:

- Runtime prerequisite: Python 3.11+.
- Command-line surface and any extra local control surface.
- The three feeds: `alpha`, `bravo`, and `charlie`.
- State or fixture storage.
- Freshness threshold and bad-configuration assumptions.
- Observability path: command output, logs, metrics, screenshots, or workflow
  output.
- CI minimum: setup, tests, smoke, and candidate documentation validation.

Minimum implementation scope is intentionally small: a local runnable freshness
model, deterministic scenario commands, tests, smoke validation, CI evidence,
and written operating notes. Do not substitute future platform plans for the
local behavior.

## Separate liveness from eligibility

Document how the system answers two different questions:

- **Liveness:** can the feed consumer answer?
- **Safe-to-serve eligibility:** may unsafe downstream work continue?

Use the same field names the implementation exposes. At minimum, cover `alive`,
`last_tick_age_seconds`, `freshness_status`, `safe_to_serve`,
`allowed_actions`, and `blocked_reason`.

Expected-state contract:

| State | Required architecture behavior |
| --- | --- |
| Healthy feeds | All feeds are fresh and safe to serve. |
| Stale `bravo` | `bravo` fails closed, with a reason tied to age threshold. |
| Unknown `bravo` tick age | `bravo` fails closed, with a reason tied to missing age. |
| Partial availability | `alpha` and `charlie` stay eligible while `bravo` is unsafe. |
| Recovered `bravo` | Recovery returns the system to eligible status. |

Canonical unsafe actions are `price_order`, `publish_signal`, and
`rebalance_position`. Explain why those actions must be blocked for stale or
unknown data and which read-only or inspection actions remain safe.

## Describe feed boundaries

Describe what makes one feed distinct from another. Include identity,
configuration, dependency boundary, health-state ownership, and blast-radius
assumptions.

## State design tradeoffs

List the important choices you made and why. Separate implemented behavior from
future production work.

Reviewers will evaluate five senior dimensions:

- Reliability model.
- Incident response.
- Automation, CI/CD, and recovery.
- Observability and actionability.
- Tradeoffs and restraint.

Don't turn future production ideas into implemented claims.
