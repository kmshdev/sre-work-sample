# 2026 Site Reliability Engineering Work Sample

Open the live assignment packet first:
<https://kmshdev.github.io/sre-work-sample/>.

Build a small local system that shows how you would operate a critical runtime
platform. The reviewer must be able to clone your repository, run your commands,
trigger failures, inspect evidence, and understand your tradeoffs.

The assessment window is **7 calendar days**.

## Table of contents

- [Starter baseline](#the-starter-gives-you-a-runnable-baseline)
- [Assignment files](#the-assignment-files-have-one-job-each)
- [Runtime slice](#your-task-is-to-operate-three-simulated-runtimes)
- [Hard gates](#the-hard-gates-must-pass-before-review)
- [Health model](#the-health-model-must-fail-closed)
- [Evidence](#evidence-must-make-behavior-reproducible)
- [Failure scenarios](#failure-scenarios-must-show-detection-and-recovery)
- [Release safety](#release-safety-must-show-blast-radius-control)
- [Submission report](#the-report-must-separate-facts-from-plans)
- [Constraints](#the-constraints-keep-the-review-local-and-safe)
- [AI usage](#ai-tool-use-must-be-disclosed-and-verified)
- [No-agent incident](#the-no-agent-incident-answer-must-be-written-by-you)
- [Follow-up interview](#the-follow-up-interview-will-test-your-tradeoffs)

## The starter gives you a runnable baseline

This repository is a starter template, not a solution. It includes a small
Python scaffold so the first checkout already has tests, a smoke command, and a
place for evidence.

Run the starter before changing it:

```sh
make setup
make test
make smoke
make run
```

The starter includes:

- `src/sre_work_sample/` for the local runtime model and control surface.
- `tests/` for behavior tests.
- `docs/ARCHITECTURE.md` for system shape and tradeoffs.
- `docs/OPERATIONS.md` for runbooks, alerts, and recovery steps.
- `evidence/` for logs, screenshots, transcripts, and command output.
- `.github/workflows/validate.yml` for repeatable validation.
- `SUBMISSION.md`, `AI_USAGE.md`, `NO_AGENT_INCIDENT.md`, and
  `DEFENSE_NOTES.md` placeholders.

You may replace the scaffold if another stack makes the work clearer. Keep the
fresh-checkout path and smoke command working.

## The assignment files have one job each

Use the files below as the main reading path:

| File | Purpose |
| --- | --- |
| `index.html` | Browser entry point for the candidate packet. |
| `README.md` | Authoritative assignment specification. |
| `CANDIDATE_RUNBOOK.html` | Suggested work sequence for the 7-day window. |
| `HEALTH_MODEL_GUIDE.html` | Guidance for liveness, safety, and blocked work. |
| `EVIDENCE_AND_VALIDATION_GUIDE.html` | Guidance for proof and rerunnable commands. |
| `SUBMISSION_TEMPLATE.md` | Structure for the final report in `SUBMISSION.md`. |
| `AI_USAGE.md` | Disclosure and verification notes for AI-assisted work. |
| `NO_AGENT_INCIDENT.md` | Human-written incident response segment. |
| `DEFENSE_NOTES.md` | Notes for the follow-up technical discussion. |

## Your task is to operate three simulated runtimes

Build the smallest local slice that proves your operating model.

Your implementation must include:

- One operator control surface, such as a command-line interface, local web
  page, terminal interface, or local application programming interface.
- Three simulated runtimes with separate identities or configuration.
- One mock external dependency, such as a fake data feed, account service,
  gateway, queue, or platform service.
- One pause or block operation that prevents unsafe work without deleting state.
- Health states for the states exercised by your implementation.
- A repeatable delivery path that runs validation and smoke checks.
- Two operational failure scenarios implemented end to end.
- One bad rollout or bad configuration scenario tied to release safety.

Use fake data and local services. Don't connect to real customer, production
account, payment, or secret-bearing systems.

## The hard gates must pass before review

The reviewer will stop early if the hard gates are missing.

- **Fresh checkout:** setup, start, smoke, and cleanup commands in `SUBMISSION.md`.
- **Smoke command:** one command that checks control, runtimes, dependency, and
  health in `SUBMISSION.md`.
- **Delivery path:** repeatable validation and release-safety evidence in a
  workflow, script, or transcript.
- **Health model:** clear split between liveness and safe operation in
  `docs/ARCHITECTURE.md`.
- **Two failures:** trigger, detection, blocked work, recovery, and evidence in
  `evidence/` and `SUBMISSION.md`.
- **Release safety:** bad rollout or bad config implemented end to end in
  `SUBMISSION.md`.
- **No-agent incident:** human-written incident response in `NO_AGENT_INCIDENT.md`.

If a command needs a specific tool version, fake environment variable, or local
data file, document it before the command.

## The health model must fail closed

A running process isn't always safe to operate.

Separate two questions:

- **Process liveness:** Can the runtime answer?
- **Operational eligibility:** Is the runtime safe to perform unsafe work?

Define only the states your slice uses. Common examples include:

- `healthy`
- `degraded_dependency`
- `degraded_data_stale`
- `paused_by_operator`
- `incident_active`
- `maintenance_or_rollout`

For each state, document:

- The signal that enters the state.
- What the operator sees.
- Which actions remain allowed.
- Which actions are blocked.
- Which alert, ticket, annotation, or runbook applies.
- How the runtime exits the state.

Use [`HEALTH_MODEL_GUIDE.html`](HEALTH_MODEL_GUIDE.html) for examples.

## Evidence must make behavior reproducible

Evidence should let another engineer inspect what happened and rerun what
matters.

Useful evidence includes:

- Commands with expected output or captured output.
- Structured logs with runtime, state, dependency, and timestamp.
- Metric samples or dashboard screenshots.
- Workflow runs or local validation transcripts.
- Failure-trigger commands and recovery commands.
- Short notes that explain what each artifact proves.

Use [`EVIDENCE_AND_VALIDATION_GUIDE.html`](EVIDENCE_AND_VALIDATION_GUIDE.html)
to check evidence quality.

## Failure scenarios must show detection and recovery

Implement two operational failure scenarios end to end.

Good scenario choices include:

- A runtime crash or restart.
- A mock dependency outage or timeout.
- Stale data while the runtime process is still alive.
- A reconciliation failure or mismatched local state.
- A bad rollout or bad configuration affecting only part of the fleet.

For each implemented scenario, show:

- How to trigger the failure.
- How the system detects the failure.
- Which runtime or platform state changes.
- What becomes blocked and what remains allowed.
- Which alert, ticket, annotation, or runbook path applies.
- How to recover.
- Which evidence proves the scenario worked.

Document any scenarios you intentionally defer. Explain how you would implement
and validate them with more time.

## Release safety must show blast-radius control

One of the two implemented failure scenarios must be a bad rollout or bad
configuration.

The release-safety scenario must show validation, promotion or rejection,
rollback, and blast-radius control. Document any additional release-safety ideas
as future work.

Kubernetes, Terraform, Helm, and GitOps are optional. Use them only if they make
the local evidence clearer.

## The report must separate facts from plans

Use [`SUBMISSION_TEMPLATE.md`](SUBMISSION_TEMPLATE.md) for your final report.
Replace `SUBMISSION.md` with your completed report.

Your report must include:

- What you built.
- How to run it from a fresh checkout.
- Smoke command and expected output.
- Health states and blocked actions.
- Two implemented failure scenarios.
- Release-safety scenario evidence.
- Delivery automation evidence.
- Security and operator-control assumptions.
- What you intentionally didn't build.
- What you would do next with more time.
- Links to `AI_USAGE.md`, `NO_AGENT_INCIDENT.md`, and `DEFENSE_NOTES.md`.

## The constraints keep the review local and safe

Follow these constraints:

- Don't include real secrets.
- Don't require paid infrastructure.
- Don't depend on real external accounts.
- Don't hide failure behind restart-only recovery.
- Don't make the assignment depend on one vendor unless the reason is clear.
- Don't add broad production scope that your evidence doesn't exercise.
- Don't spend time on visual polish at the cost of operational evidence.

## AI tool use must be disclosed and verified

AI coding tools are allowed, but you own the output.

If you use AI tools, complete `AI_USAGE.md` with:

- Tool names.
- What you asked the tools to do.
- Generated changes you accepted, edited, or rejected.
- One generated result that was wrong or incomplete.
- How you caught the problem.
- Verification you ran yourself.

If you don't use AI tools, state that in `AI_USAGE.md` and `SUBMISSION.md`.

## The no-agent incident answer must be written by you

Complete `NO_AGENT_INCIDENT.md` without coding agents or large language models.

Use normal documentation, shell tools, man pages, and your own notes. The file
should show how you reason during the first 30 minutes of an incident.

## The follow-up interview will test your tradeoffs

Expect questions about:

- Why you chose your stack.
- How your health model blocks unsafe work.
- What your alerts page on and what they deliberately don't page on.
- How your delivery path supports validation, promotion, and rollback.
- How the local slice would grow to 20-50 runtimes.
- How you used or avoided AI tools.
- What you would change before production.

Invite `kmshdev` as a collaborator or reviewer only after the report and
evidence are ready.
