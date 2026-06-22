from sre_work_sample.freshness import evaluate_system, healthy_state, set_feed_age


def test_healthy_feeds_are_eligible() -> None:
    status = evaluate_system(healthy_state())

    assert status["overall_status"] == "eligible"
    assert status["unsafe_feeds"] == []
    assert all(feed["safe_to_serve"] for feed in status["feeds"])


def test_stale_feed_fails_closed_without_blocking_fresh_feeds() -> None:
    stale_state = set_feed_age(healthy_state(), "bravo", 660)
    status = evaluate_system(stale_state)
    feeds = {feed["name"]: feed for feed in status["feeds"]}

    assert status["overall_status"] == "restricted"
    assert status["unsafe_feeds"] == ["bravo"]
    assert feeds["bravo"]["freshness_status"] == "stale"
    assert not feeds["bravo"]["safe_to_serve"]
    assert "price_order" in feeds["bravo"]["blocked_actions"]
    assert feeds["alpha"]["safe_to_serve"]
    assert feeds["charlie"]["safe_to_serve"]


def test_recovered_feed_restores_eligibility() -> None:
    stale_state = set_feed_age(healthy_state(), "bravo", 660)
    recovered_state = set_feed_age(stale_state, "bravo", 5)
    status = evaluate_system(recovered_state)

    assert status["overall_status"] == "eligible"
    assert status["unsafe_feeds"] == []


def test_unknown_feed_is_actionable_error() -> None:
    try:
        set_feed_age(healthy_state(), "delta", 5)
    except ValueError as error:
        assert "unknown feed" in str(error)
    else:
        raise AssertionError("expected unknown feed to raise ValueError")
