# SRE Take-Home: Market Data Freshness

This is the starter template for a senior SRE take-home assignment. You will
operate a small local market-data freshness system with three fictional feeds:
`alpha`, `bravo`, and `charlie`.

Your goal is not to build a trading platform. Your goal is to show that stale
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

Expected smoke result:

```json
{
  "checks": [
    "healthy feeds eligible",
    "stale bravo fails closed",
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
| `DEFENSE_NOTES.md` | Notes for follow-up technical discussion. |

You may change the starter code. Keep setup, tests, smoke, and docs validation
working from a fresh checkout.

## Required candidate flow

Use this flow to prove the assignment end to end:

1. Run `make setup`.
2. Run `make test`.
3. Run `make smoke`.
4. Show healthy status for `alpha`, `bravo`, and `charlie`.
5. Trigger a stale `bravo` scenario.
6. Show `bravo` is unsafe while `alpha` and `charlie` remain eligible.
7. Recover `bravo`.
8. Show the recovered state is eligible.
9. Push or otherwise show GitHub Actions evidence.
10. Complete `SUBMISSION.md`, `INCIDENT_NOTE.md`, `AI_USAGE.md`, and
    `DEFENSE_NOTES.md`.

Useful direct commands:

```sh
.venv/bin/python -m sre_work_sample.cli status
tmp=/tmp/bravo-stale.json
.venv/bin/python -m sre_work_sample.cli scenario stale --feed bravo --output "$tmp"
.venv/bin/python -m sre_work_sample.cli status --state /tmp/bravo-stale.json
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
- `make smoke` proves healthy, stale, and recovered states.
- GitHub Actions runs setup, tests, smoke, and docs validation.
- A stale feed is detected.
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

## Evidence to submit

Prefer command output, JSON, test output, CI links, and short notes. Evidence
should let another engineer rerun your proof without guessing.

Include evidence for:

- Healthy baseline.
- Stale `bravo` or another explicitly chosen feed.
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

- Do not include real secrets.
- Do not require paid infrastructure.
- Do not depend on real external accounts.
- Do not connect to real trading, broker, exchange, or customer systems.
- Do not hide failure behind restart-only recovery.
- Do not make Kubernetes, Terraform, DNS, BGP, or cloud deployment required.
- Do not trade operational evidence for dashboard polish.

## AI usage

AI coding tools are allowed. You own the output.

If you use AI tools, complete `AI_USAGE.md` with:

- Tool names.
- What you asked the tools to do.
- Generated changes you accepted, edited, or rejected.
- One generated result that was wrong or incomplete.
- How you caught the problem.
- Verification you ran yourself.

If you do not use AI tools, state that in `AI_USAGE.md` and `SUBMISSION.md`.

## Follow-up interview

Be ready to discuss:

- Why your model blocks unsafe work.
- Which stale-data alert pages and which alert only creates a ticket.
- How a freshness threshold would roll out safely.
- How the model would scale beyond three feeds.
- What Kubernetes, Terraform, CI/CD, or edge infrastructure would add later.
- What AI suggestion you rejected or corrected.
- What you would change before production.

Invite `kmshdev` as a collaborator or reviewer only after the report and
evidence are ready.
