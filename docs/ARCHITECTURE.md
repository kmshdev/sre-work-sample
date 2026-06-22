# Architecture Notes

Use this file to explain the freshness service you built. The reviewer should
learn what runs locally, where state lives, and which tradeoffs are intentional.

## Explain the local system shape

Cover:

- Command-line surface and any extra local control surface.
- The three feeds: `alpha`, `bravo`, and `charlie`.
- State or fixture storage.
- Freshness threshold and bad-configuration assumptions.
- Observability path: command output, logs, metrics, screenshots, or workflow
  output.

## Separate liveness from eligibility

Document how the system answers two different questions:

- **Liveness:** can the feed consumer answer?
- **Safe-to-serve eligibility:** may unsafe downstream work continue?

Use the same field names the implementation exposes. At minimum, cover `alive`,
`last_tick_age_seconds`, `freshness_status`, `safe_to_serve`,
`allowed_actions`, and `blocked_reason`.

## Describe feed boundaries

Describe what makes one feed distinct from another. Include identity,
configuration, dependency boundary, health-state ownership, and blast-radius
assumptions.

## State design tradeoffs

List the important choices you made and why. Separate implemented behavior from
future production work.

Do not turn future production ideas into implemented claims.
