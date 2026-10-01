import json
import struct

PROTOCOL_VERSION = 1

HEADER_SIZE = 4

MSG_HELLO = "hello"
MSG_INTENT = "intent"
MSG_SNAPSHOT = "snapshot"


def encode(message) -> bytes:
    """
    This function serialize a message to a length-prefixed frame.
    :param message: Message as a plain dict
    :return: Frame bytes (4-byte length header + JSON body)
    """
    body = json.dumps(message).encode("utf-8")
    header = struct.pack("!I", len(body))

    return header + body


def decode(buffer) -> list:
    """
    This function decode as many complete messages as possible from a buffer.
    :param buffer: Bytes received so far
    :return: (messages, remaining_buffer)
    """
    messages = []

    while len(buffer) >= HEADER_SIZE:
        (length,) = struct.unpack("!I", buffer[:HEADER_SIZE])

        if len(buffer) < HEADER_SIZE + length:
            break

        body = buffer[HEADER_SIZE:HEADER_SIZE + length]
        messages.append(json.loads(body.decode("utf-8")))
        buffer = buffer[HEADER_SIZE + length:]

    return messages, buffer


def make_hello() -> dict:
    """
    This function build a hello message with the protocol version.
    :return: Hello message
    """
    return {"type": MSG_HELLO, "version": PROTOCOL_VERSION}


def make_intent(intents) -> dict:
    """
    This function build an intent message.
    :param intents: Collection of action strings (ex. "left", "zoom_in")
    :return: Intent message
    """
    return {"type": MSG_INTENT, "intents": sorted(set(intents))}


def make_snapshot(snapshot) -> dict:
    """
    This function build a snapshot message.
    :param snapshot: World state as a dict
    :return: Snapshot message
    """
    return {"type": MSG_SNAPSHOT, "state": snapshot}
