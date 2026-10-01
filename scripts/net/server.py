import asyncio

from scripts import settings as s
from scripts.net import protocol
from scripts.world import WorldModel

TICK_RATE = 20
TICK_DT = 1000 / TICK_RATE


class Server:
    """
    Authoritative game server.
    Owns the world model, applies client intents and broadcasts snapshots.
    """

    def __init__(self, world=None) -> None:
        self.world = world or WorldModel()
        self.clients = set()
        self.intents = {}  # player_id -> set of action strings
        self._next_player_id = 0

    def new_player_id(self) -> str:
        """
        This function allocate a unique player id for a new connection.
        :return: A unique player id
        """
        player_id = str(self._next_player_id)
        self._next_player_id += 1

        return player_id

    async def handle_client(self, reader, writer) -> None:
        self.clients.add(writer)
        player_id = self.new_player_id()
        self.world.add_player(player_id)
        self.intents[player_id] = set()

        try:
            await self.send(writer, protocol.make_snapshot(self.world.snapshot()))

            while True:
                data = await reader.read(s.NET_BUFFER_SIZE)

                if not data:
                    break

                messages, _ = protocol.decode(data)

                for message in messages:
                    if message["type"] == protocol.MSG_INTENT:
                        self.intents[player_id] = set(message["intents"])
        except (ConnectionResetError, asyncio.IncompleteReadError):
            pass
        finally:
            self.clients.discard(writer)
            self.world.remove_player(player_id)
            self.intents.pop(player_id, None)
            writer.close()

    async def send(self, writer, message) -> None:
        writer.write(protocol.encode(message))
        await writer.drain()

    async def broadcast(self, message) -> None:
        frame = protocol.encode(message)

        for writer in list(self.clients):
            try:
                writer.write(frame)
                await writer.drain()
            except (ConnectionResetError, BrokenPipeError):
                self.clients.discard(writer)

    async def tick(self) -> None:
        self.world.step_players(TICK_DT, self.intents)
        self.intents = {player_id: set() for player_id in self.intents}
        await self.broadcast(protocol.make_snapshot(self.world.snapshot()))

    async def run(self, host=s.NET_HOST, port=s.NET_PORT) -> None:
        self._server = await asyncio.start_server(self.handle_client, host, port)

        async with self._server:
            await self._server.start_serving()

            while True:
                await asyncio.sleep(TICK_DT / 1000)
                await self.tick()

    @property
    def port(self) -> int:
        """
        This function return the bound port (useful when binding port 0).
        :return: Bound port
        """
        return self._server.sockets[0].getsockname()[1]


def run(host=s.NET_HOST, port=s.NET_PORT) -> None:
    """
    This function run the server until interrupted (blocking).
    :param host: Host to bind
    :param port: Port to bind
    :return: None
    """
    asyncio.run(Server().run(host, port))
