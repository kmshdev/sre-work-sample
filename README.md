# 2026 SRE Take-Home: Critical Runtime Operations Platform

Open [`index.html`](index.html) as the browser entry point for this assignment
packet. This README remains the authoritative assignment specification. Use
[`CANDIDATE_RUNBOOK.html`](CANDIDATE_RUNBOOK.html) as a pacing guide,
[`HEALTH_MODEL_GUIDE.html`](HEALTH_MODEL_GUIDE.html) for health-state guidance,
[`EVIDENCE_AND_VALIDATION_GUIDE.html`](EVIDENCE_AND_VALIDATION_GUIDE.html) for
proof expectations, and [`SUBMISSION_TEMPLATE.md`](SUBMISSION_TEMPLATE.md) for
your final report.

This take-home is a senior SRE work sample over 7 calendar days for someone who
would help operate a small but critical runtime fleet. We do not expect production
breadth. We do expect a clear operational model, repeatable local evidence,
release-safety thinking, and tradeoffs you can defend.

## Starter scaffold

This repository includes a small Python 3.11 starter scaffold so you have a
fresh-checkout path on day one. It is not a completed solution. Replace or extend
it as needed.

```sh
make setup
make test
make smoke
make run
```

The scaffold gives you:

- `src/sre_work_sample/` for the local control surface and runtime-fleet model.
- `tests/` for behavior tests.
- `docs/` for architecture and operations notes.
- `evidence/` for captured proof artifacts.
- `.github/workflows/validate.yml` for repeatable validation.
- `SUBMISSION.md`, `AI_USAGE.md`, `NO_AGENT_INCIDENT.md`, and
  `DEFENSE_NOTES.md` placeholders.

## Core premise

This repository provides only a starter scaffold, not the assessment
implementation. Build or assemble the smallest local system needed to
demonstrate your operational model.

Your submission must run from a fresh checkout without paid infrastructure or
real external accounts. Use fake data, local services, disposable resources, and
mock integrations only.

The real-world shape is a platform with 20-50 independent runtime instances. A
runtime is a single workload with its own identity, configuration, health, and
external dependency boundary. The platform must help an operator answer:

- Which runtimes are safe to operate now?
- Which runtimes are degraded, paused, blocked, or in incident response?
- Which actions are allowed when data, dependencies, or rollout state are
  uncertain?
- How would the team detect, recover, roll back, and learn from failure?

Your implementation should be the smallest local slice that proves those ideas.

## Required implementation scope

Implement or assemble a local runtime-fleet slice with:

- One control surface, such as an API, CLI, dashboard, terminal UI, or simple
  web surface.
- Three simulated runtimes with separate identities or configuration.
- One mock dependency, such as a data feed, account-status service, broker
  simulator, gateway, or equivalent fake external service.
- One pause or block operation that prevents unsafe work without deleting state.
- Health states for the states exercised by your implemented slice.
- A repeatable delivery automation path.
- Two implemented operational failure scenarios end to end.
- One bad rollout or bad configuration scenario tied to release safety.
- Documented plans for remaining scenarios you would implement with more time.

Implement two failure scenarios end to end. Document how you would implement and
validate the remaining scenarios with more time.

The release-safety scenario may count as one of the two implemented scenarios if
it is demonstrated end to end. If it is not implemented end to end, document it
separately with enough detail that a reviewer can see the intended validation,
promotion, rollback, and blast-radius controls.

Depth matters more than breadth. A small, well-evidenced slice is stronger than a
large system whose behavior cannot be started, observed, failed, and recovered
locally.

## Fresh-checkout evidence

Your submission must include exact commands that work from a fresh checkout.
Assume the reviewer has cloned your repository on a new machine and has no prior
local state.

Include:

- Prerequisites and supported versions.
- Setup commands.
- Start commands.
- A smoke command that verifies the control surface, runtimes, mock dependency,
  and at least one health-state response.
- Cleanup commands.
- Expected output or evidence for each command.

These fresh-checkout run commands and the smoke command are hard gates. If a
reviewer cannot follow them without paid infrastructure or real external
accounts, the submission will not proceed.

## Delivery automation

Include a repeatable delivery automation path. It can use GitHub Actions, GitLab
CI, CircleCI, Jenkins, Buildkite, ArgoCD, Flux, Make, Taskfile, or equivalent
automation, but it must show setup, validation, smoke checks, promotion or
deploy, and rollback thinking.

This does not need to be a large production pipeline. It does need to prove that
you can turn reliability expectations into repeatable automation. Include
evidence such as workflow YAML, Make or Taskfile targets, CI logs, local dry-run
output, smoke-test output, or deployment transcripts.

Delivery automation evidence is a hard gate.

## Health model

Use [`HEALTH_MODEL_GUIDE.html`](HEALTH_MODEL_GUIDE.html) to define how your
runtime health model separates process liveness from operational eligibility.
Process liveness says a runtime can answer. Operational eligibility says it is
safe for the runtime to do unsafe work.

Define the states your slice exercises. Include only states you can explain
clearly, but cover the implemented failure scenarios and pause or block behavior.
Common states include:

- `starting`
- `healthy`
- `degraded_dependency`
- `degraded_data_stale`
- `blocked_reconciliation_failed`
- `paused_by_operator`
- `incident_active`
- `maintenance_or_rollout`

For each state you use, document:

- Entry signals.
- What the operator sees.
- Which actions are allowed, paused, or blocked.
- Which alert, ticket, annotation, or runbook path applies.
- How the runtime recovers or exits the state.

A health endpoint returning success is not enough. The model must make unsafe
unknowns visible and fail closed.

## Observability and alerting

Use [`EVIDENCE_AND_VALIDATION_GUIDE.html`](EVIDENCE_AND_VALIDATION_GUIDE.html)
to keep evidence concrete. Observability is vendor-neutral for this assignment.
OpenTelemetry-style concepts, Prometheus-compatible metrics, structured logs,
plain JSON, dashboards, screenshots, and command output are all acceptable when
they are clear and repeatable.

Include enough evidence for another engineer to understand what happened:

- Health commands or endpoints.
- Metrics or equivalent signals for runtime state, dependency health, data
  freshness, error rate, restart count, and rollout or configuration status.
- Structured or searchable logs.
- Suggested SLIs and SLOs for availability, freshness, recovery, and incident
  response.
- At least three alert definitions or documented alert rules with threshold,
  severity, owner, and action.
- Evidence from a short run, such as command output, screenshots, log excerpts,
  dashboard JSON, or metric samples.

We value SRE and DORA-aligned thinking: fast detection, low blast radius,
recoverability, clear rollback criteria, meaningful alerts, and reliability
targets that help the team make decisions.

## Failure scenarios

Implement two operational failure scenarios end to end. At least one scenario
must also demonstrate release safety through a bad rollout, bad configuration,
or controlled promotion failure, unless you document the release-safety scenario
separately as described above.

Useful scenarios include:

- Runtime crash or restart.
- Mock dependency outage or timeout.
- Stale data while the runtime process is still alive.
- Reconciliation failure or mismatched local state.
- Bad rollout or bad configuration affecting only a subset of runtimes.

For each implemented scenario, show:

- How to trigger it.
- How the platform detects it.
- Which runtime or platform state changes.
- What becomes blocked and what remains allowed.
- Which alert, ticket, annotation, or incident path fires.
- How to recover.
- Which evidence proves the scenario worked.

For scenarios you do not implement, document how you would implement and validate
them with more time. Be explicit about tradeoffs.

## Deployment and rollout thinking

Document how your local slice would grow into operating 20-50 runtimes. Include:

- Runtime identity and isolation strategy.
- Configuration and secret-management assumptions.
- Rollout rings, canary, or promotion strategy.
- Rollback criteria and recovery steps.
- Backup or state-recovery approach where relevant.
- What Kubernetes, Terraform, Helm, GitOps, or cloud services would add if you
  chose to use them.
- Why you did or did not use those tools in the local work sample.

Kubernetes and Terraform are relevant, but optional. Use them only if they help
your evidence and do not make review depend on paid infrastructure.

## Security and operator controls

Document how privileged operations should work. Include:

- Authentication and authorization assumptions.
- Actions that need audit logs.
- Actions that need confirmation or two-person review.
- How secrets and external account identifiers would be protected.
- What should never be allowed directly from a browser or unaudited client.

## AI coding tools

AI coding tools are allowed, but you own their output. We will evaluate how you
supervised, verified, and corrected generated work.

If you use tools such as Codex, Claude Code, Cursor, Copilot, or similar tools,
include `AI_USAGE.md` with:

- Which tools you used.
- What you asked them to do.
- Which generated changes you accepted, edited, or rejected.
- One example where generated work was wrong or incomplete and how you caught it.
- The verification you ran yourself.

If you do not use AI tools, state that in your submission report.

## No-agent incident segment

Create `NO_AGENT_INCIDENT.md` without using coding agents or LLMs. You may use
normal documentation, man pages, shell tools, and your own notes.

Answer this prompt in your own words:

> At 09:37, the operator surface is reachable and API latency is normal, but
> charts have not updated for 11 minutes for 9 of 50 runtimes. Runtime processes
> are still running. Operators ask whether they should pause affected runtimes.
> What do you do in the first 30 minutes?

Include:

- Your first five checks.
- The severity you would declare and why.
- What you would block or allow.
- Who you would page or notify.
- The operator-facing status message.
- The first runbook action.
- What evidence would let you close or downgrade the incident.

## Submission report

Include a concise submission report. You may use
[`SUBMISSION_TEMPLATE.md`](SUBMISSION_TEMPLATE.md). The report must include:

- Architecture overview.
- Fresh-checkout setup and run commands.
- Smoke command and output.
- What you implemented.
- What you intentionally did not implement.
- Implemented failure-scenario evidence.
- Planned remaining scenarios.
- Delivery automation evidence.
- Rollout, rollback, and recovery notes.
- Security and operator-control notes.
- AI usage log or a statement that you did not use AI tools.
- Validation evidence.
- Follow-up questions you would ask the team.

Also create `DEFENSE_NOTES.md` with:

- Three design decisions you expect to defend.
- One thing you would redesign with more time.
- One generated mistake you caught, or a statement that you did not use AI tools.
- One unresolved production risk.
- The strongest evidence artifact in your submission.

## Constraints

- Do not connect to real trading, broker, exchange, customer, or secret-bearing
  systems.
- Do not include real secrets.
- Do not require paid infrastructure to review your submission.
- Do not make the assignment depend on one specific vendor unless you explain
  why.
- Do not hide failures behind restarts only. A restart can be part of recovery,
  but it cannot be the whole health model.
- Do not spend time making a beautiful UI at the cost of reliability evidence.
- Do not implement speculative production breadth that your evidence does not
  exercise.

## What we will evaluate

This take-home is an asynchronous filter. Passing it means we should spend
interview time with you; it is not a final hiring decision.

We will evaluate:

- Reliability judgment under ambiguity.
- Fresh-checkout operability.
- Delivery automation quality.
- Health-state design and fail-closed behavior.
- Observability quality and alert actionability.
- Incident response and runbook clarity.
- Rollout, recovery, and rollback thinking.
- Security and operator-control boundaries.
- How you use or do not use AI coding tools.
- How clearly you communicate tradeoffs.

Hard gates for proceeding:

- Fresh-checkout setup and run commands.
- Smoke command with expected output.
- Delivery automation evidence.
- Clear health model that separates process liveness from operational
  eligibility.
- Two implemented operational failure scenarios, including or accompanied by a
  bad rollout or bad configuration scenario tied to release safety.
- Documented plans for remaining scenarios.
- Credible `NO_AGENT_INCIDENT.md`.
- Assignment constraints respected.

Automatic reject examples:

- Treating a basic liveness response as the full health model.
- No failure injection evidence.
- Restart-only recovery.
- Vague alerts without thresholds, severity, owner, or action.
- Missing `NO_AGENT_INCIDENT.md`.
- Undisclosed or unverified AI-heavy work.
- Real external account or secret integrations.
- Paid infrastructure required for review.
- Missing fresh-checkout or smoke evidence.
- Missing delivery automation evidence.

We will not evaluate:

- Vendor spend.
- Pixel-perfect UI design.
- Algorithm puzzles.
- Whether you chose our preferred stack.
- Whether every future production feature is implemented.

## Suggested working plan

Day 1:

- Read the assignment and companion guides.
- Choose the smallest stack that can prove the operational model.
- Sketch the architecture, health model, and delivery automation path.

Day 2:

- Build the control surface, simulated runtimes, mock dependency, and pause or
  block operation.
- Add health states, logs, metrics, and alerts for the first implemented
  scenario.

Day 3:

- Add the second implemented failure scenario and the release-safety evidence.
- Add the smoke command and fresh-checkout validation path.

Day 4-5:

- Write runbooks, rollout notes, security notes, and the no-agent incident
  segment.
- Run the delivery automation path and capture evidence.

Day 6-7:

- Tighten documentation, remove accidental scope, rerun smoke checks, and prepare
  for the follow-up interview.

## Follow-up interview

In the follow-up interview, expect us to ask:

- Why you chose your stack and what you would change in production.
- How your health model prevents unsafe action when truth is stale.
- What your alerts page on and what they deliberately do not page on.
- How your delivery automation supports validation, promotion, and rollback.
- How you would operate 20-50 runtimes with a small SRE team.
- How you used AI tools and how you verified their output.
- How you handled the no-agent incident prompt.

Bring your repository, run instructions, delivery evidence, and any screenshots
or logs needed to show the system working.
