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
    assert server.intents == {}


def test_new_player_id_is_unique():
    server = Server()

    first = server.new_player_id()
    second = server.new_player_id()

    assert first != second


def test_tick_applies_per_player_intents_and_resets_them():
    server = Server(make_world(distance=10))
    server.world.add_player("0")
    server.intents = {"0": {"right"}}

    asyncio.run(server.tick())

    assert server.world.players["0"].x == pytest.approx(1 * TICK_DT / 1000)
    assert server.intents == {"0": set()}


def test_client_creates_its_own_player_over_socket():
    async def scenario():
        server = Server(make_world())
        task = asyncio.create_task(server.run("127.0.0.1", 0))
        await asyncio.sleep(0.05)

        client = NetClient("127.0.0.1", server.port)
        client.update(0, [])
        await asyncio.sleep(0.1)

        player_ids = set()
        for _ in range(20):
            snapshot = client.receive_snapshot()
            if snapshot and snapshot.get("players"):
                player_ids = set(snapshot["players"])
                break
            await asyncio.sleep(0.05)

        client.close()
        task.cancel()
        return player_ids

    player_ids = asyncio.run(scenario())

    assert player_ids == {"0"}


def test_two_clients_see_each_others_players():
    async def scenario():
        server = Server(make_world())
        task = asyncio.create_task(server.run("127.0.0.1", 0))
        await asyncio.sleep(0.05)

        first = NetClient("127.0.0.1", server.port)
        second = NetClient("127.0.0.1", server.port)
        first.update(0, ["right"])
        second.update(0, ["right"])
        await asyncio.sleep(0.2)

        snapshot = None
        for _ in range(20):
            snapshot = first.receive_snapshot()
            if snapshot and len(snapshot.get("players", {})) == 2:
                break
            await asyncio.sleep(0.05)

        first.close()
        second.close()
        task.cancel()
        return snapshot

    snapshot = asyncio.run(scenario())

    assert snapshot is not None
    assert set(snapshot["players"]) == {"0", "1"}


def test_player_is_removed_when_client_disconnects():
    async def scenario():
        server = Server(make_world())
        task = asyncio.create_task(server.run("127.0.0.1", 0))
        await asyncio.sleep(0.05)

        client = NetClient("127.0.0.1", server.port)
        client.update(0, [])
        await asyncio.sleep(0.1)
        client.close()
        await asyncio.sleep(0.1)

        players = dict(server.world.players)
        task.cancel()
        return players

    players = asyncio.run(scenario())

    assert players == {}
