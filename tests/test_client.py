import pytest

from scripts.camera import CameraModel
from scripts.net.client import Client, LocalClient, NetClient
from scripts.world import WorldModel


def make_world(x=0, y=0, distance=10, resolution=(1000, 500)):
    camera = CameraModel(x=x, y=y, distance=distance, resolution=resolution)
    world = WorldModel(camera_model=camera)
    world.add_player("0")
    return world


def test_local_client_is_a_client():
    assert isinstance(LocalClient(make_world()), Client)


def test_local_client_update_steps_world():
    world = make_world(x=5, distance=10)
    client = LocalClient(world)

    client.update(1000, ["right"])

    assert world.players["0"].x == pytest.approx(1)


def test_local_client_update_returns_world_snapshot():
    world = make_world(x=1, y=2, distance=3, resolution=(800, 600))
    world.players["0"].color = (10, 20, 30)
    client = LocalClient(world)

    snapshot = client.update(0, [])

    assert snapshot["camera"] == {"x": 1, "y": 2, "distance": 3, "resolution": [800, 600]}
    assert snapshot["field"] == {}
    assert snapshot["players"] == {"0": {"x": 0, "y": 0, "color": [10, 20, 30], "size": 2}}


def test_local_client_close_is_a_noop():
    client = LocalClient(make_world())

    client.close()


def test_net_client_is_a_client():
    assert issubclass(NetClient, Client)
