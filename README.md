# SRE Take-Home: Market Data Freshness

This is the starter template for a senior SRE take-home assignment. You'll
operate a small local market-data freshness system with three fictional feeds:
`alpha`, `bravo`, and `charlie`.

Your goal isn't to build a trading platform. Your goal is to show that stale
data is detected, unsafe work fails closed, healthy feeds remain eligible, and
recovery can be reproduced by another engineer.

The assessment window is **7 calendar days**. Use the window to produce a
reviewable system, evidence, and tradeoff notes rather than a large feature set.

Last reviewed: 2026-06-22.

## Table of contents

- [Start here](#start-here)
- [What you are building](#what-you-are-building)
- [What is already in the repo](#what-is-already-in-the-repo)
- [Required candidate flow](#required-candidate-flow)
- [Hard gates](#hard-gates)
- [Health model](#health-model)
- [Evidence to submit](#evidence-to-submit)
- [Incident prompt](#incident-prompt)
- [Constraints](#constraints)
- [AI usage](#ai-usage)
- [Follow-up interview](#follow-up-interview)

## Start here

Run the baseline before changing anything:

```sh
make setup
make test
make smoke
```

Prerequisites:

- Python 3.11+.
- A POSIX-like shell for `make` and `scripts/smoke.sh`.
- GitHub Actions or equivalent CI that runs setup, tests, smoke, and docs check.

Expected smoke result:

```json
{
  "checks": [
    "healthy feeds eligible",
    "stale bravo fails closed",
    "unknown data fails closed",
    "alpha and charlie remain eligible",
    "bravo recovery restores eligibility"
  ],
  "smoke": "passed"
}
```

This README is the assignment source of truth. Use `SUBMISSION_TEMPLATE.md` as
the report structure, replace `SUBMISSION.md` with your completed report, and
keep setup, tests, smoke, and docs validation working from a fresh checkout.

## What you are building

Build a small local system that makes market-data freshness operationally clear.
At minimum, your implementation must show:

- All three feeds have a visible status.
- A feed can be alive while its data is stale.
- Stale or unknown data blocks unsafe downstream work.
- If `bravo` is stale, `alpha` and `charlie` can remain eligible.
- Recovery restores eligibility through a rerunnable command or workflow.
- Tests, smoke output, GitHub Actions, and written evidence prove the behavior.

Minimum implementation scope:

- Keep the assignment runnable locally with Python 3.11+.
- Preserve a CLI path for healthy, stale, unknown, and recovered states.
- Keep `make test`, `make smoke`, and `make docs-check` passing.
- Keep CI at least as strict as local validation: install, test, smoke, docs check.
- Document the reliability model, runbook, alerting, automation, and tradeoffs.

## What is already in the repo

| Path | Purpose |
| --- | --- |
| `src/sre_work_sample/` | Starter Python package and CLI entry points. |
| `tests/` | Behavior tests for the starter freshness model. |
| `data/healthy.json` | Simple healthy-state fixture. |
| `docs/ARCHITECTURE.md` | Fill this with health-model and design notes. |
| `docs/OPERATIONS.md` | Fill this with runbooks, alerts, and recovery notes. |
| `.github/workflows/validate.yml` | CI workflow for tests, smoke, and docs checks. |
| `SUBMISSION_TEMPLATE.md` | Suggested structure for `SUBMISSION.md`. |
| `SUBMISSION.md` | Your completed submission report. |
| `INCIDENT_NOTE.md` | Your first-30-minute stale-feed incident note. |
| `AI_USAGE.md` | AI tool disclosure and verification notes. |
| `FOLLOWUP_NOTES.md` | Notes for follow-up technical discussion. |

You may change the starter code. Keep setup, tests, smoke, and docs validation
working from a fresh checkout.

## Required candidate flow

Use this flow to prove the assignment end to end:

1. Run `make setup`.
2. Run `make test`.
3. Run `make smoke`.
4. Show healthy status for `alpha`, `bravo`, and `charlie`.
5. Trigger a stale `bravo` scenario.
6. Trigger an unknown tick-age `bravo` scenario.
7. Show `bravo` is unsafe while `alpha` and `charlie` remain eligible.
8. Recover `bravo`.
9. Show the recovered state is eligible.
10. Push or otherwise show GitHub Actions evidence.
11. Complete `SUBMISSION.md`, `INCIDENT_NOTE.md`, `AI_USAGE.md`, and
    `FOLLOWUP_NOTES.md`.

Useful direct commands:

```sh
.venv/bin/python -m sre_work_sample.cli status
tmp=/tmp/bravo-stale.json
.venv/bin/python -m sre_work_sample.cli scenario stale --feed bravo --output "$tmp"
.venv/bin/python -m sre_work_sample.cli status --state /tmp/bravo-stale.json
.venv/bin/python -m sre_work_sample.cli scenario unknown \
  --feed bravo \
  --output /tmp/bravo-unknown.json
.venv/bin/python -m sre_work_sample.cli status --state /tmp/bravo-unknown.json
.venv/bin/python -m sre_work_sample.cli recover \
  --feed bravo \
  --state /tmp/bravo-stale.json \
  --output /tmp/bravo-recovered.json
.venv/bin/python -m sre_work_sample.cli status --state /tmp/bravo-recovered.json
```

## Hard gates

The reviewer may stop early if any hard gate fails:

- Fresh checkout setup works.
- `make test` passes.
- `make smoke` proves healthy, stale, unknown, partial-availability, and recovered states.
- GitHub Actions runs setup, tests, smoke, and docs validation.
- A stale feed is detected.
- Unknown tick age is detected.
- Unsafe downstream work fails closed.
- Unaffected fresh feeds remain eligible during partial failure.
- Recovery is reproducible.
- `INCIDENT_NOTE.md` is credible and concise.
- No real accounts, secrets, paid services, or cloud deployment are required.

## Health model

Separate liveness from safe-to-serve eligibility.

Make these fields visible in code, CLI output, tests, docs, or evidence:

- `alive`: whether the feed consumer can answer.
- `last_tick_age_seconds`: age of the newest known tick.
- `freshness_status`: `fresh`, `stale`, or `unknown`.
- `safe_to_serve`: whether unsafe downstream work may continue.
- `allowed_actions`: work still permitted for the feed.
- `blocked_reason`: why unsafe work is blocked.

The important distinction: a process can be alive and still unsafe because its
data is stale.

Expected-state contract:

| State | Required outcome |
| --- | --- |
| Healthy `alpha`, `bravo`, `charlie` | `freshness_status=fresh`, `safe_to_serve=true`. |
| Stale `bravo` | `freshness_status=stale`, `safe_to_serve=false`, unsafe work blocked. |
| Unknown `bravo` tick age | `freshness_status=unknown`, not safe, blocked reason present. |
| Partial availability | Fresh `alpha` and `charlie` remain safe while `bravo` is unsafe. |
| Recovered `bravo` | All feeds return to `overall_status=eligible`. |

Canonical unsafe action set:

- `price_order`
- `publish_signal`
- `rebalance_position`

## Evidence to submit

Prefer command output, JSON, test output, CI links, and short notes. Evidence
should let another engineer rerun your proof without guessing.

Include evidence for:

- Healthy baseline.
- Stale `bravo` or another explicitly chosen feed.
- Unknown tick-age scenario.
- Blocked unsafe action.
- Continued eligibility for unaffected feeds.
- Recovery output.
- GitHub Actions validation.
- Alert rationale: what pages, what creates a ticket, and why.
- Bad-config detection or rollback judgment.

## Incident prompt

Answer this prompt in `INCIDENT_NOTE.md` or inside `SUBMISSION.md`:

> At 09:37, the service is reachable and latency is normal, but `bravo` has not
> received fresh ticks for 11 minutes. `alpha` and `charlie` are fresh.
> Operators ask whether downstream work should continue. What do you do in the
> first 30 minutes?

Cover severity, first checks, block/allow decision, notification,
operator-facing status, first runbook action, and closure evidence.

## Constraints

Keep the review local and safe:

- Don't include real secrets.
- Don't require paid infrastructure.
- Don't depend on real external accounts.
- Don't connect to real trading, broker, exchange, or customer systems.
- Don't hide failure behind restart-only recovery.
- Don't make Kubernetes, Terraform, DNS, BGP, or cloud deployment required.
- Don't trade operational evidence for cosmetic polish.

## AI usage

AI coding tools are allowed. You own the output.

If you use AI tools, complete `AI_USAGE.md` with:

- Tool names.
- What you asked the tools to do.
- Generated changes you accepted, edited, or rejected.
- One generated result that was wrong or incomplete.
- How you caught the problem.
- Verification you ran yourself.

If you don't use AI tools, state that in `AI_USAGE.md` and `SUBMISSION.md`.

## Follow-up interview

Be ready to discuss:

- Reliability model: how liveness, freshness, and safe-to-serve decisions differ.
- Incident response: how operators classify, communicate, mitigate, and close.
- Automation, CI/CD, and recovery: how validation and rollback stay repeatable.
- Observability and actionability: whether signals lead to clear operator actions.
- Tradeoffs and restraint: what you intentionally avoided and why.
- Why your model blocks unsafe work.
- Which stale-data alert pages and which alert only creates a ticket.
- How a freshness threshold would roll out safely.
- How the model would scale beyond three feeds.
- What Kubernetes, Terraform, CI/CD, or edge infrastructure would add later.
- What AI suggestion you rejected or corrected.
- What you would change before production.

Invite `kmshdev` as a collaborator or reviewer only after the report and
evidence are ready.
