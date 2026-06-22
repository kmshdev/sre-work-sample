# Operations notes

Use this file for runbooks, alert notes, rollout decisions, and recovery
procedures.

The reviewer should learn what an operator sees, what they do next, and which
commands prove the system recovered. Keep commands concrete enough to run from
a fresh checkout.

## Fresh-checkout commands

List setup, start, smoke, and cleanup commands with expected output.

## Failure scenarios

For each implemented scenario, include the trigger, detection signal, blocked
action, recovery step, and evidence location.

## Alerts and operator actions

For each alert, include threshold, severity, owner, and first action. Avoid
alerts that tell an operator something is wrong without telling them what to do.

Don't include alerts that your local evidence never exercises.
