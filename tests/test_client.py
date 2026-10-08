import pytest

from scripts.camera import CameraModel
from scripts.net.client import Client, InterpolatingClient, LocalClient, NetClient
from scripts.world import WorldModel


def make_world(x=0, y=0, distance=10, resolution=(1000, 500)):
    camera = CameraModel(x=x, y=y, distance=distance, resolution=resolution)
    return WorldModel(camera_model=camera)


def test_local_client_is_a_client():
    assert isinstance(LocalClient(make_world()), Client)


def test_local_client_update_steps_world():
    client = LocalClient(make_world(x=5, distance=10))

    client.update(1000, ["right"])

    assert client.world.camera_model.x == pytest.approx(15)


def test_local_client_update_returns_world_snapshot():
    client = LocalClient(make_world(x=1, y=2, distance=3, resolution=(800, 600)))

    snapshot = client.update(0, [])

    assert snapshot == {
        "camera": {"x": 1, "y": 2, "distance": 3, "resolution": [800, 600]},
        "field": {},
    }


def test_local_client_close_is_a_noop():
    client = LocalClient(make_world())

    client.close()


def test_net_client_is_a_client():
    assert issubclass(NetClient, Client)


class FakeClient(Client):
    def __init__(self, snapshots=()) -> None:
        self.snapshots = list(snapshots)
        self.latest = None
        self.closed = False

    def update(self, dt, intents):
        if self.snapshots:
            self.latest = self.snapshots.pop(0)

        return self.latest  # same object while nothing new arrives (like NetClient)

    def close(self) -> None:
        self.closed = True


def make_snapshot(x):
    return {"camera": {"x": x, "y": 0, "distance": 10, "resolution": [800, 600]}, "field": {}}


def test_interpolating_client_is_a_client():
    assert isinstance(InterpolatingClient(FakeClient()), Client)


def test_interpolating_client_returns_none_before_any_snapshot():
    client = InterpolatingClient(FakeClient(), interval_ms=100)

    assert client.update(16, []) is None


def test_interpolating_client_passes_the_first_snapshot_through():
    client = InterpolatingClient(FakeClient([make_snapshot(0)]), interval_ms=100)

    snapshot = client.update(0, [])

    assert snapshot["camera"]["x"] == 0


def test_interpolating_client_blends_between_two_snapshots():
    client = InterpolatingClient(FakeClient([make_snapshot(0), make_snapshot(10)]), interval_ms=100)

    client.update(0, [])
    snapshot = client.update(50, [])

    assert snapshot["camera"]["x"] == pytest.approx(5)


def test_interpolating_client_keeps_advancing_without_a_new_snapshot():
    client = InterpolatingClient(FakeClient([make_snapshot(0), make_snapshot(10)]), interval_ms=100)

    client.update(0, [])   # first snapshot
    client.update(40, [])  # second snapshot arrives, alpha 0.4
    snapshot = client.update(35, [])  # no new packet, clock must keep running (alpha 0.75)

    assert snapshot["camera"]["x"] == pytest.approx(7.5)


def test_interpolating_client_does_not_interpolate_resolution():
    client = InterpolatingClient(FakeClient([make_snapshot(0), make_snapshot(10)]), interval_ms=100)

    client.update(0, [])
    snapshot = client.update(50, [])

    assert snapshot["camera"]["resolution"] == [800, 600]


def test_interpolating_client_close_closes_the_wrapped_client():
    wrapped = FakeClient()
    client = InterpolatingClient(wrapped, interval_ms=100)

    client.close()

    assert wrapped.closed
