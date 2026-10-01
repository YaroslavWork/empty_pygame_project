import json

from scripts.field import FieldModel


def test_to_dict_is_json_serializable():
    field = FieldModel()

    assert json.loads(json.dumps(field.to_dict())) == field.to_dict()


def test_snapshot_roundtrip():
    field = FieldModel()

    field.from_dict(field.to_dict())

    assert field.to_dict() == {}