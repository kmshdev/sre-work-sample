# Architecture notes

Use this file to explain the shape of the system you built. The reviewer should
learn what runs locally, where state lives, and which tradeoffs are intentional.

## System shape

- Control surface.
- Three simulated runtimes and their identities.
- Mock dependency.
- Pause or block operation.
- State or configuration storage.
- Observability path.

## Runtime boundaries

Describe what makes one runtime distinct from another. Include identity,
configuration, dependency boundary, and health-state ownership.

## Design tradeoffs

List the important choices you made and why. Separate implemented behavior from
future production work.

Don't turn future production ideas into implemented claims.
