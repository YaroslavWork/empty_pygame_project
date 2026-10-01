import socket

from scripts.net import protocol


class Client:
    """
    Interface of a client connection.
    Both singleplayer and multiplayer use this interface, so the game code
    never needs to know whether the world runs locally or on a server.
    """

    def send_intents(self, intents) -> None:
        raise NotImplementedError

    def receive_snapshot(self):
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


class LocalClient(Client):
    """
    Client that talks to an in-process world model (singleplayer).
    It uses the same interface as NetClient, so gameplay code is identical.
    """

    def __init__(self, world) -> None:
        self.world = world

    def send_intents(self, intents) -> None:
        pass

    def step(self, dt, intents) -> None:
        self.world.step(dt, intents)

    def receive_snapshot(self):
        return self.world.snapshot()

    def close(self) -> None:
        pass


class NetClient(Client):
    """
    Client that talks to a remote server over TCP.
    Sends intents and receives the latest world snapshot.
    """

    def __init__(self, host, port) -> None:
        self.socket = socket.create_connection((host, port))
        self.socket.setblocking(False)
        self.buffer = b""
        self.latest_snapshot = None

    def send_intents(self, intents) -> None:
        self.socket.sendall(protocol.encode(protocol.make_intent(intents)))

    def receive_snapshot(self):
        try:
            data = self.socket.recv(4096)
        except BlockingIOError:
            return self.latest_snapshot

        if not data:
            return self.latest_snapshot

        self.buffer += data
        messages, self.buffer = protocol.decode(self.buffer)

        for message in messages:
            if message["type"] == protocol.MSG_SNAPSHOT:
                self.latest_snapshot = message["state"]

        return self.latest_snapshot

    def close(self) -> None:
        self.socket.close()

