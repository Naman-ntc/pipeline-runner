import pytest
from datetime import datetime
from api.serializers import serialize_model, deserialize_request, validate_fields


class FakeModel:
    def __init__(self, name, created_at, count):
        self.name = name
        self.created_at = created_at
        self.count = count


def test_serialize_model_with_datetime():
    obj = FakeModel("test", datetime(2024, 1, 15, 10, 30), 42)
    result = serialize_model(obj)
    assert result["name"] == "test"
    assert result["created_at"] == "2024-01-15T10:30:00"
    assert result["count"] == 42


def test_serialize_model_with_none_value():
    obj = FakeModel("test", None, 5)
    result = serialize_model(obj)
    assert result["name"] == "test"
    assert result["created_at"] is None
    assert result["count"] == 5


def test_serialize_model_skips_private():
    obj = FakeModel("x", datetime(2024, 6, 1), 1)
    obj._internal = "hidden"
    result = serialize_model(obj)
    assert "_internal" not in result


def test_deserialize_json():
    body = b'{"key": "value", "num": 42}'
    result = deserialize_request(body)
    assert result == {"key": "value", "num": 42}


def test_deserialize_form_urlencoded():
    body = b"name=alice&role=admin"
    result = deserialize_request(body, "application/x-www-form-urlencoded")
    assert result["name"] == "alice"
    assert result["role"] == "admin"


def test_deserialize_unsupported_content_type():
    with pytest.raises(ValueError, match="Unsupported"):
        deserialize_request(b"data", "text/xml")


def test_validate_fields_all_present():
    errors = validate_fields({"name": "alice", "email": "a@b.com"}, ["name", "email"])
    assert errors == []


def test_validate_fields_missing():
    errors = validate_fields({"name": "x"}, ["name", "email"])
    assert len(errors) == 1
    assert "email" in errors[0]


def test_validate_fields_empty_value():
    errors = validate_fields({"name": ""}, ["name"])
    assert len(errors) == 1
    assert "empty" in errors[0].lower()
