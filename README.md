# SRE Take-Home: Market Data Freshness

Open the live assignment packet first:
<https://kmshdev.github.io/sre-work-sample/artifacts/>.

This repository is the starter template for the assignment. It gives you a small
Python command-line application, three fictional market-data feeds, tests, and a
GitHub Actions workflow. Your job is to make the local system operationally
credible.

The assessment window is **6 calendar days**. Expect **6-8 focused hours**.

## Table of contents

- [Start with the runnable baseline](#start-with-the-runnable-baseline)
- [Use each assignment file for one job](#use-each-assignment-file-for-one-job)
- [Make freshness the operating problem](#make-freshness-the-operating-problem)
- [Pass the hard gates first](#pass-the-hard-gates-first)
- [Separate liveness from safe-to-serve eligibility](#separate-liveness-from-safe-to-serve)
- [Show evidence another engineer can rerun](#show-evidence-another-engineer-can-rerun)
- [Use GitHub Actions as the delivery gate](#use-github-actions-as-the-delivery-gate)
- [Write the incident note in the submission](#write-the-incident-note-in-the-submission)
- [Keep the review local and safe](#keep-the-review-local-and-safe)
- [Disclose AI tool use](#disclose-ai-tool-use)
- [Prepare for the follow-up interview](#prepare-for-the-follow-up-interview)

## Start with the runnable baseline

Run the starter before changing it:

```sh
make setup
make test
make smoke
```

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

The starter includes:

- `src/sre_work_sample/` for the freshness model and command-line interface.
- `tests/` for behavior tests.
- `data/healthy.json` for a simple fixture.
- `docs/ARCHITECTURE.md` for health-model and design notes.
- `docs/OPERATIONS.md` for runbooks, alerts, and recovery steps.
- `evidence/` for logs, screenshots, transcripts, and command output.
- `.github/workflows/validate.yml` for repeatable validation.
- `SUBMISSION.md`, `AI_USAGE.md`, `INCIDENT_NOTE.md`, and `DEFENSE_NOTES.md`
  placeholders.

You may change the starter. Keep the fresh-checkout path and smoke command
working.

## Use each assignment file for one job

| File | Purpose |
| --- | --- |
| `artifacts/index.html` | Single-page browser guide for the candidate packet. |
| `README.md` | Authoritative assignment specification. |
| `SUBMISSION_TEMPLATE.md` | Structure for the final report in `SUBMISSION.md`. |
| `SUBMISSION.md` | Your completed report. |
| `AI_USAGE.md` | Disclosure and verification notes for AI-assisted work. |
| `INCIDENT_NOTE.md` | Concise first-30-minute incident response note. |
| `DEFENSE_NOTES.md` | Notes for the follow-up technical discussion. |

## Make freshness the operating problem

The fictional service has three market-data feeds:

- `alpha`
- `bravo`
- `charlie`

Each feed can be alive while its data is stale. A process that answers requests
is not automatically safe for downstream work.

Your implementation must show:

- A status view for all three feeds.
- Stale data detection for at least one feed.
- Fail-closed behavior when a feed is stale or unknown.
- A recovery path that restores eligibility.
- A bad-configuration or rollback-safety note.
- Observability evidence: freshness signal, liveness signal, page threshold, and
  ticket threshold.

## Pass the hard gates first

The reviewer will stop early if a hard gate fails.

- **Fresh checkout:** setup, test, smoke, and cleanup commands work.
- **Local tests:** `make test` passes.
- **Smoke command:** `make smoke` proves healthy, stale, and recovered states.
- **GitHub Actions:** the workflow runs setup, tests, smoke, and docs validation.
- **Stale feed behavior:** one feed can fail closed while others remain eligible.
- **Recovery:** a reviewer can reproduce recovery from a stale feed state.
- **Incident note:** `INCIDENT_NOTE.md` or the submission report answers the
  incident prompt.
- **Constraints:** no real accounts, paid services, or secrets are required.

## Separate liveness from safe-to-serve

Use `docs/ARCHITECTURE.md` and the evaluation section in `artifacts/index.html`
to explain the health model.

At minimum, make these fields visible:

- `alive`: whether the feed consumer can answer.
- `last_tick_age_seconds`: age of the newest known tick.
- `freshness_status`: `fresh`, `stale`, or `unknown`.
- `safe_to_serve`: whether unsafe downstream work may continue.
- `allowed_actions`: work still permitted for the feed.
- `blocked_reason`: why unsafe work is blocked.

Strong submissions make partial failure obvious. If only `bravo` is stale,
`bravo` should fail closed while `alpha` and `charlie` remain eligible.

## Show evidence another engineer can rerun

Evidence should be concrete. Prefer command output, workflow logs, JSON, test
output, and short notes over long prose.

Include evidence for:

- Healthy status.
- Stale `bravo` or another chosen feed.
- Blocked unsafe actions.
- Recovery.
- GitHub Actions validation.
- Alert thresholds and owner/action notes.

Use the evidence task section in `artifacts/index.html` to check evidence
quality.

## Use GitHub Actions as the delivery gate

GitHub Actions is required. The included workflow runs:

- Python install.
- Unit tests.
- Smoke check.
- Candidate documentation validation.

You may extend the workflow. Keep it fast and deterministic.

## Write the incident note in the submission

Answer this prompt in `INCIDENT_NOTE.md` or inside `SUBMISSION.md`:

> At 09:37, the service is reachable and latency is normal, but `bravo` has not
> received fresh ticks for 11 minutes. `alpha` and `charlie` are fresh.
> Operators ask whether downstream work should continue. What do you do in the
> first 30 minutes?

Cover severity, first five checks, the block/allow decision, notification,
operator-facing status, first runbook action, and closure evidence.

## Keep the review local and safe

Follow these constraints:

- Do not include real secrets.
- Do not require paid infrastructure.
- Do not depend on real external accounts.
- Do not connect to real trading, broker, exchange, or customer systems.
- Do not hide failure behind restart-only recovery.
- Do not make Kubernetes, Terraform, DNS, BGP, or cloud deployment required.
- Do not spend time on visual polish at the cost of operational evidence.

## Disclose AI tool use

AI coding tools are allowed. You own the output.

If you use AI tools, complete `AI_USAGE.md` with:

- Tool names.
- What you asked the tools to do.
- Generated changes you accepted, edited, or rejected.
- One generated result that was wrong or incomplete.
- How you caught the problem.
- Verification you ran yourself.

If you do not use AI tools, state that in `AI_USAGE.md` and `SUBMISSION.md`.

## Prepare for the follow-up interview

Expect questions about:

- How the health model blocks unsafe work.
- Which alert pages and which alert only creates a ticket.
- How to roll out a feed freshness threshold safely.
- How the model would scale from three feeds to many feed boundaries.
- What Kubernetes, Terraform, managed continuous integration, or edge
  infrastructure would add.
- How you used or avoided AI tools.
- What you would change before production.

Invite `kmshdev` as a collaborator or reviewer only after the report and
evidence are ready.
