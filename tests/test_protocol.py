import json

from scripts.net import protocol


def test_encode_starts_with_length_header():
    frame = protocol.encode({"type": "hello"})

    length = int.from_bytes(frame[:4], "big")

    assert length == len(frame) - 4


def test_encode_is_json_body():
    frame = protocol.encode({"type": "hello"})

    assert json.loads(frame[4:].decode("utf-8")) == {"type": "hello"}


def test_decode_single_message():
    frame = protocol.encode({"type": "hello", "version": 1})

    messages, rest = protocol.decode(frame)

    assert messages == [{"type": "hello", "version": 1}]
    assert rest == b""


def test_decode_multiple_messages():
    buffer = protocol.encode({"a": 1}) + protocol.encode({"b": 2})

    messages, rest = protocol.decode(buffer)

    assert messages == [{"a": 1}, {"b": 2}]
    assert rest == b""


def test_decode_keeps_incomplete_message():
    frame = protocol.encode({"a": 1})

    messages, rest = protocol.decode(frame[:3])

    assert messages == []
    assert rest == frame[:3]


def test_decode_keeps_partial_body():
    frame = protocol.encode({"a": 1})

    messages, rest = protocol.decode(frame[:-1])

    assert messages == []
    assert rest == frame[:-1]


def test_decode_complete_plus_partial():
    buffer = protocol.encode({"a": 1}) + protocol.encode({"b": 2})[:2]

    messages, rest = protocol.decode(buffer)

    assert messages == [{"a": 1}]
    assert rest == protocol.encode({"b": 2})[:2]


def test_roundtrip_make_hello():
    message = protocol.make_hello()

    messages, _ = protocol.decode(protocol.encode(message))

    assert messages == [{"type": protocol.MSG_HELLO, "version": protocol.PROTOCOL_VERSION}]


def test_roundtrip_make_intent_dedupes_and_sorts():
    message = protocol.make_intent(["right", "left", "right"])

    messages, _ = protocol.decode(protocol.encode(message))

    assert messages == [{"type": protocol.MSG_INTENT, "intents": ["left", "right"]}]


def test_roundtrip_make_snapshot():
    state = {"camera": {"x": 1}, "field": {}}
    message = protocol.make_snapshot(state)

    messages, _ = protocol.decode(protocol.encode(message))

    assert messages == [{"type": protocol.MSG_SNAPSHOT, "state": state}]
