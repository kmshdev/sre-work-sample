# Candidate submission template

Read the live assignment packet before filling this out:
<https://kmshdev.github.io/sre-work-sample/>.

You may use this template for your final report. Keep it concise and link to
commands, logs, screenshots, dashboards, workflow runs, or files where they are
clearer than prose.

## 1. Summary

State what you built in 5-8 sentences. Include the stack, the local runtime-fleet
slice, the main reliability idea, and what a reviewer should run first.

## 2. Architecture overview

Describe:

- Control surface.
- Three simulated runtimes and their identities.
- Mock dependency.
- Pause or block operation.
- State or configuration storage.
- Observability path.

Include a small diagram if it helps.

## 3. Fresh-checkout setup and run commands

Assume the reviewer has cloned the repository on a new machine with no prior
local state. List exact commands and expected output or evidence.

Fresh-checkout path:

```sh
git clone <repository-url>
cd <repository-directory>
```

Prerequisites and supported versions:

```text
<tool and version list>
```

Setup commands:

```sh
<commands>
```

Start commands:

```sh
<commands>
```

Cleanup commands:

```sh
<commands>
```

If any local review path needs environment variables, fake data, or disposable
resources, document them here.

## 4. Smoke command and output

Provide the smoke command that verifies the control surface, simulated runtimes,
mock dependency, and at least one health-state response.

Command:

```sh
<smoke command>
```

Expected output or captured output:

```text
<output>
```

## 5. Health model

Define only the states exercised by your implemented slice. Show how the model
separates process liveness from operational eligibility.

| State | Entry signal | Operator view | Allowed | Blocked | Alert or runbook | Exit |
| --- | --- | --- | --- | --- | --- | --- |
| healthy | | | | | | |
| paused_by_operator | | | | | | |
| <state> | | | | | | |

## 6. Observability and alerting

Document:

- Health commands or endpoints.
- Metrics or equivalent signals.
- Structured or searchable logs.
- Suggested SLIs and SLOs.
- At least three alert rules with threshold, severity, owner, and action.
- Evidence from a short run.

## 7. Implemented failure scenarios

Include two end-to-end implemented operational failure scenarios. One scenario
must demonstrate release safety through a bad rollout or bad configuration.

For each scenario, include:

- Trigger command or action.
- Detection signal.
- State transition.
- What becomes blocked and what remains allowed.
- Alert, ticket, annotation, or incident path.
- Recovery command or action.
- Evidence that proves the scenario worked.

### Scenario 1: <name>

### Scenario 2: <name>

## 8. Planned future scenarios

List scenarios you intentionally didn't implement. For each one, explain how
you would implement and validate it with more time, plus the tradeoff that led
you to defer it.

## 9. Delivery automation evidence

Link to or paste evidence for the repeatable delivery path. Include:

- Automation entry point, such as workflow, Make target, Taskfile, or equivalent.
- Setup and validation steps.
- Smoke checks.
- Promotion or deploy step.
- Rollback or recovery thinking.
- CI logs, local dry-run output, workflow output, or deployment transcript.

## 10. Deployment, rollout, and recovery notes

Explain how the local slice would grow to 20-50 runtimes:

- Runtime identity and isolation strategy.
- Configuration and secret-management assumptions.
- Rollout rings, canary, or promotion strategy.
- Rollback criteria and recovery steps.
- Backup or state-recovery approach where relevant.
- What Kubernetes, Terraform, Helm, GitOps, or cloud services would add, if you
  would use them.
- Why you did or didn't use those tools in the local work sample.

## 11. Security and operator controls

Describe:

- Authentication and authorization assumptions.
- Actions that need audit logs.
- Actions that need confirmation or two-person review.
- Secret and external account identifier handling.
- Operations that should never be allowed from an unaudited client.

## 12. No-agent incident declaration

Link to `NO_AGENT_INCIDENT.md`.

Confirm that the file was completed without coding agents or LLMs. Summarize the
severity, first five checks, blocked or allowed actions, notifications,
operator-facing status message, first runbook action, and closure evidence.

## 13. AI usage

Link to `AI_USAGE.md`, or state that you didn't use AI tools.

If you used AI tools, include:

- Tool names.
- Prompts or task descriptions.
- Generated changes you accepted, edited, or rejected.
- One wrong or incomplete generated result and how you caught it.
- Verification you ran yourself.

## 14. Tradeoffs and omissions

List what you intentionally didn't build and why. Include the next changes you
would make with more time.

## 15. Follow-up defense notes

Link to `DEFENSE_NOTES.md`.

Confirm that it includes:

- Three design decisions you expect to defend.
- One thing you would redesign with more time.
- One generated mistake you caught, or a statement that you didn't use AI tools.
- One unresolved production risk.
- The strongest evidence artifact in your submission.
- The most important questions you would ask before productionizing the platform.
