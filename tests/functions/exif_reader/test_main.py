import io
from unittest.mock import Mock

import pytest

from exif_reader import main, geo
from helpers import file_as_buffer


ddb_mock = None


@pytest.fixture
def mock_ddb(monkeypatch):
    global ddb_mock
    ddb_mock = Mock()
    monkeypatch.setattr('exif_reader.main.ddb', ddb_mock)

def test_handler_no_object(monkeypatch):
    utils_mock = Mock()
    monkeypatch.setattr('exif_reader.main.utils', utils_mock)

    event = {'weird': 'payload'}
    main.handler(event, {})

    assert utils_mock.fetch_from_bucket.call_count == 0

def test_handler_no_exif_data(monkeypatch, mock_ddb):
    fetch_mock = Mock(return_value=io.BytesIO(b'0xdeadbeef'))
    monkeypatch.setattr('exif_reader.main.utils.fetch_from_bucket',
                        fetch_mock)

    event = {'Records': [{'s3': {'object': {'key': 'not/an/image.txt'}}}]}
    main.handler(event, {})

    assert fetch_mock.call_count == 1
    assert ddb_mock.store_exif_data.call_count == 0

def test_handler_exif_no_geo(monkeypatch, mock_ddb):
    fetch_mock = Mock(return_value=file_as_buffer('./matterhorn.png'))
    monkeypatch.setattr('exif_reader.main.utils.fetch_from_bucket',
                        fetch_mock)

    event = {'Records': [{'s3': {'object': {'key': 'matterhorn.png'}}}]}
    main.handler(event, {})

    assert fetch_mock.call_count == 1
    assert ddb_mock.store_exif_data.call_count == 1
    (object_key, exif_data), _kwargs = ddb_mock.store_exif_data.call_args
    assert object_key == 'matterhorn.png'
    assert isinstance(exif_data, dict)

    assert ddb_mock.store_coordinate.call_count == 0

def test_handler_exif_with_geo(monkeypatch, mock_ddb):
    fetch_mock = Mock(return_value=file_as_buffer('./happydog.jpg'))
    monkeypatch.setattr('exif_reader.main.utils.fetch_from_bucket',
                        fetch_mock)

    event = {'Records': [{'s3': {'object': {'key': 'happydog.jpg'}}}]}
    main.handler(event, {})

    assert fetch_mock.call_count == 1
    assert ddb_mock.store_exif_data.call_count == 1
    (object_key, exif_data), _kwargs = ddb_mock.store_exif_data.call_args
    assert object_key == 'happydog.jpg'
    assert isinstance(exif_data, dict)

    assert ddb_mock.store_coordinate.call_count == 1
    (object_key, coord), _kwargs = ddb_mock.store_coordinate.call_args
    assert object_key == 'happydog.jpg'
    assert isinstance(coord, geo.Coordinate)
    assert pytest.approx(coord.lat, 8.1428277777777)
    assert pytest.approx(coord.lng, 79.709686111111)
