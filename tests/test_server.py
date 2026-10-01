import asyncio

import pytest

from scripts.camera import CameraModel
from scripts.net import protocol
from scripts.net.client import NetClient
from scripts.net.server import Server, TICK_DT
from scripts.world import WorldModel


def make_world(x=0, y=0, distance=10, resolution=(1000, 500)):
    camera = CameraModel(x=x, y=y, distance=distance, resolution=resolution)
    return WorldModel(camera_model=camera)


def test_server_starts_with_a_world():
    server = Server()

    assert isinstance(server.world, WorldModel)
    assert server.clients == set()
    assert server.intents == set()


def test_tick_applies_intents_and_resets_them():
    server = Server(make_world(x=5, distance=10))
    server.intents = {"right"}

    asyncio.run(server.tick())

    assert server.world.camera_model.x == pytest.approx(5 + 1 * 10 * TICK_DT / 1000)
    assert server.intents == set()


def test_intent_roundtrip_over_socket():
    async def scenario():
        server = Server(make_world(x=5, distance=10))
        task = asyncio.create_task(server.run("127.0.0.1", 0))
        await asyncio.sleep(0.05)

        client = NetClient("127.0.0.1", server.port)
        client.update(0, ["right"])
        await asyncio.sleep(0.1)

        snapshot = None
        for _ in range(20):
            snapshot = client.receive_snapshot()
            if snapshot and snapshot["camera"]["x"] > 5:
                break
            await asyncio.sleep(0.05)

        client.close()
        task.cancel()
        return snapshot

    snapshot = asyncio.run(scenario())

    assert snapshot is not None
    assert snapshot["camera"]["x"] > 5
