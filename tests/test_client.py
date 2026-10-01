import pytest

from scripts.camera import CameraModel
from scripts.net.client import Client, LocalClient, NetClient
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
