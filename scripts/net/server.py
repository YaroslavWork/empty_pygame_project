import asyncio

from scripts import settings as s
from scripts.net import protocol
from scripts.world import WorldModel

TICK_RATE = 20  # simulation steps per second (a snapshot is broadcast every tick)
TICK_DT = 1000 / TICK_RATE  # length of one tick in milliseconds


class Server:
    """
    Authoritative game server.
    Owns the world model, applies client intents and broadcasts snapshots.
    """

    def __init__(self, world=None) -> None:
        """
        This function build the server.
        It owns the authoritative world, the connected clients and the intents
        collected since the previous tick.
        :param world: World model to run (a fresh WorldModel when not given)
        :return: None
        """
        self.world = world or WorldModel()
        self.clients = set()  # writers of every connected client
        self.intents = set()  # intents received since the last tick

    async def handle_client(self, reader, writer) -> None:
        """
        This function serve one connected client until it disconnects.
        It sends the current world state right away (so the client can render
        before the first tick), collects the intents the client sends and drops
        the connection when it goes away.
        :param reader: Stream to read messages from the client
        :param writer: Stream to write messages to the client
        :return: None
        """
        self.clients.add(writer)

        try:
            # Send a snapshot immediately, otherwise the client waits a full tick
            await self.send(writer, protocol.make_snapshot(self.world.snapshot()))

            while True:
                data = await reader.read(s.NET_BUFFER_SIZE)

                if not data:
                    break  # an empty read means the client closed the connection

                messages, _ = protocol.decode(data)  # leftover bytes are not needed here

                for message in messages:
                    if message["type"] == protocol.MSG_INTENT:
                        self.intents.update(message["intents"])  # applied on the next tick
        except (ConnectionResetError, asyncio.IncompleteReadError):
            pass  # the client dropped: fall through to the cleanup below
        finally:
            self.clients.discard(writer)
            writer.close()

    async def send(self, writer, message) -> None:
        """
        This function write one message to a single client and wait until it is flushed.
        :param writer: Stream to write the message to
        :param message: Message as a plain dict
        :return: None
        """
        writer.write(protocol.encode(message))
        await writer.drain()

    async def broadcast(self, message) -> None:
        """
        This function send the same message to every connected client.
        The frame is encoded once and shared between all writers, and clients
        that already dropped are removed from the list.
        :param message: Message as a plain dict
        :return: None
        """
        frame = protocol.encode(message)

        for writer in list(self.clients):  # copy: the set is modified on a broken pipe
            try:
                writer.write(frame)
                await writer.drain()
            except (ConnectionResetError, BrokenPipeError):
                self.clients.discard(writer)

    async def tick(self) -> None:
        """
        This function advance the world by one fixed tick and broadcast the result.
        The collected intents are cleared afterwards, so each intent only affects
        a single tick.
        :return: None
        """
        self.world.step(TICK_DT, self.intents)
        self.intents = set()
        await self.broadcast(protocol.make_snapshot(self.world.snapshot()))

    async def run(self, host=s.NET_HOST, port=s.NET_PORT) -> None:
        """
        This function start the server and run its game loop forever.
        New connections are handled by handle_client; this loop wakes up once per
        tick, advances the world and broadcasts it to every client.
        :param host: Host to bind
        :param port: Port to bind
        :return: None
        """
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
    print(f"Server running on {host}:{port}")
    asyncio.run(Server().run(host, port))
