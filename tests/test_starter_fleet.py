from sre_work_sample.runtime_fleet import build_starter_fleet


def test_starter_fleet_has_three_runtimes_and_dependency() -> None:
    fleet = build_starter_fleet()

    assert len(fleet.runtimes) == 3
    assert {runtime.runtime_id for runtime in fleet.runtimes} == {
        "runtime-a",
        "runtime-b",
        "runtime-c",
    }
    assert fleet.dependency.name == "mock-market-data"


def test_starter_fleet_includes_blocked_runtime_state() -> None:
    fleet = build_starter_fleet()

    blocked = [
        runtime
        for runtime in fleet.runtimes
        if not runtime.can_accept_unsafe_work
    ]

    assert len(blocked) >= 1
