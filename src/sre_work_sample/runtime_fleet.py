"""Minimal runtime-fleet model for candidates to replace and extend."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Runtime:
    """A simulated runtime instance in the local starter fleet."""

    runtime_id: str
    state: str
    can_accept_unsafe_work: bool
    note: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-safe runtime representation."""
        return {
            "runtime_id": self.runtime_id,
            "state": self.state,
            "can_accept_unsafe_work": self.can_accept_unsafe_work,
            "note": self.note,
        }


@dataclass(frozen=True)
class MockDependency:
    """A fake external dependency boundary for local validation."""

    name: str
    status: str
    latency_ms: int

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-safe dependency representation."""
        return {
            "name": self.name,
            "status": self.status,
            "latency_ms": self.latency_ms,
        }


@dataclass(frozen=True)
class RuntimeFleet:
    """Starter fleet containing three runtimes and one mock dependency."""

    runtimes: tuple[Runtime, Runtime, Runtime]
    dependency: MockDependency


def build_starter_fleet() -> RuntimeFleet:
    """Create a deterministic starter fleet for the initial smoke command."""
    return RuntimeFleet(
        runtimes=(
            Runtime(
                runtime_id="runtime-a",
                state="healthy",
                can_accept_unsafe_work=True,
                note="sample state; replace with implemented health checks",
            ),
            Runtime(
                runtime_id="runtime-b",
                state="paused_by_operator",
                can_accept_unsafe_work=False,
                note="sample pause state; wire to a real pause operation",
            ),
            Runtime(
                runtime_id="runtime-c",
                state="degraded_dependency",
                can_accept_unsafe_work=False,
                note="sample degraded state; wire to dependency behavior",
            ),
        ),
        dependency=MockDependency(
            name="mock-market-data",
            status="healthy",
            latency_ms=12,
        ),
    )
