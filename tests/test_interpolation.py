import pytest

from scripts.net.interpolation import SnapshotBuffer, blend, lerp


def test_lerp_at_zero_returns_start():
    assert lerp(10, 20, 0) == pytest.approx(10)


def test_lerp_at_one_returns_end():
    assert lerp(10, 20, 1) == pytest.approx(20)


def test_lerp_at_half_returns_midpoint():
    assert lerp(10, 20, 0.5) == pytest.approx(15)


def test_blend_interpolates_numbers_in_nested_dicts():
    previous = {"camera": {"x": 0, "y": 0}}
    current = {"camera": {"x": 10, "y": 20}}

    result = blend(previous, current, 0.5)

    assert result["camera"]["x"] == pytest.approx(5)
    assert result["camera"]["y"] == pytest.approx(10)


def test_blend_takes_discrete_values_from_current():
    previous = {"camera": {"resolution": [800, 600], "name": "old"}}
    current = {"camera": {"resolution": [1024, 768], "name": "new"}}

    result = blend(previous, current, 0.5)

    assert result["camera"]["resolution"] == [1024, 768]
    assert result["camera"]["name"] == "new"


def test_blend_does_not_interpolate_booleans():
    assert blend({"on": False}, {"on": True}, 0.5)["on"] is True


def test_blend_uses_current_when_previous_key_is_missing():
    result = blend({"camera": {}}, {"camera": {"x": 7}}, 0.5)

    assert result["camera"]["x"] == pytest.approx(7)


def test_blend_at_zero_returns_previous_numbers():
    result = blend({"x": 0}, {"x": 10}, 0)

    assert result["x"] == pytest.approx(0)


def test_buffer_sample_is_none_before_the_first_snapshot():
    buffer = SnapshotBuffer(interval_ms=100)

    assert buffer.sample() is None


def test_buffer_first_snapshot_is_passed_through():
    buffer = SnapshotBuffer(interval_ms=100)
    snapshot = {"x": 3}

    buffer.push(snapshot)

    assert buffer.sample() == snapshot


def test_buffer_blends_between_the_last_two_snapshots():
    buffer = SnapshotBuffer(interval_ms=100)
    buffer.push({"x": 0})

    buffer.push({"x": 10})
    buffer.advance(50)

    assert buffer.sample()["x"] == pytest.approx(5)


def test_buffer_alpha_clamps_at_one():
    buffer = SnapshotBuffer(interval_ms=100)

    buffer.advance(1000)

    assert buffer.alpha == 1.0


def test_buffer_alpha_is_one_without_interval():
    buffer = SnapshotBuffer(interval_ms=0)

    assert buffer.alpha == 1.0


def test_buffer_push_keeps_the_last_current_as_previous():
    buffer = SnapshotBuffer(interval_ms=100)

    buffer.push({"x": 0})
    buffer.push({"x": 10})

    assert buffer.previous == {"x": 0}
    assert buffer.current == {"x": 10}
    assert buffer.elapsed == 0


def test_buffer_starts_blend_from_previous_after_a_new_snapshot():
    buffer = SnapshotBuffer(interval_ms=100)
    buffer.push({"x": 0})

    buffer.push({"x": 10})

    assert buffer.sample()["x"] == pytest.approx(0)
