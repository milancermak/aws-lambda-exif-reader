# pylint: disable=invalid-name

import decimal
from unittest.mock import Mock

import pytest

from exif_reader import ddb, geo


def test_decimal_from_float():
    assert isinstance(ddb.decimal_from_float(1.23), decimal.Decimal)

def test_decimalize():
    d = {'string': 'hello',
         'float': 1.23}
    out = ddb.decimalize(d)

    assert isinstance(out, dict)
    assert isinstance(out['string'], str)
    assert isinstance(out['float'], decimal.Decimal)

@pytest.mark.parametrize(
    'geohash, hash_key_length, expected',
    [(100000000000000000000, 6, 100000),
     (100000000000000000000, '6', 100000),
     (100_000_000_000_000_000_000, 6, 100000),
     (1e20, 6, 100000),
     (12345678901234567890, 10, 1234567890),
     (-12345678901234567890, 10, -1234567890),
     (-12345678901234567890, '10', -1234567890)]
)
def test_generate_hash_key(geohash, hash_key_length, expected):
    hash_key = ddb.generate_hash_key(geohash, hash_key_length)
    assert hash_key == expected

def test_store_exif_data(monkeypatch):
    monkeypatch.setenv('EXIF_DATA_TABLE', 'exif_data')
    dynamodb_mock = Mock()
    monkeypatch.setattr('exif_reader.ddb.dynamodb', dynamodb_mock)
    table_mock = Mock()
    dynamodb_mock.Table.return_value = table_mock

    object_key = 'path/to/image/happydog.jpg'
    exif_data = {'SourceFile': 'happydog.jpg',
                 "EXIF:FocalLength": 4.15}

    ddb.store_exif_data(object_key, exif_data)

    assert dynamodb_mock.Table.call_count == 1
    (table_name, ), _kwargs = dynamodb_mock.Table.call_args
    assert table_name == ('exif_data')

    assert table_mock.put_item.call_count == 1
    _args, kwargs = table_mock.put_item.call_args
    assert 'Item' in kwargs
    item_values = kwargs['Item'].values()
    assert object_key in item_values

    stored_exif_data = kwargs['Item']['exif_data']
    assert 'SourceFile' in stored_exif_data
    assert 'EXIF:FocalLength' in stored_exif_data
    has_decimals = False
    for v in stored_exif_data.values():
        if isinstance(v, decimal.Decimal):
            has_decimals = True
    assert has_decimals

def test_store_coordinate(monkeypatch):
    monkeypatch.setenv('GEO_DATA_TABLE', 'geo_data')
    monkeypatch.setenv('HASH_KEY_LENGTH', 6)
    dynamodb_mock = Mock()
    monkeypatch.setattr('exif_reader.ddb.dynamodb', dynamodb_mock)
    table_mock = Mock()
    dynamodb_mock.Table.return_value = table_mock

    object_key = 'path/to/image/Matterhorn.png'
    coord = geo.Coordinate(45.9765731, 7.6409423)

    ddb.store_coordinate(object_key, coord)

    assert dynamodb_mock.Table.call_count == 1
    (table_name, ), _kwargs = dynamodb_mock.Table.call_args
    assert table_name == 'geo_data'

    assert table_mock.put_item.call_count == 1
    _args, kwargs = table_mock.put_item.call_args
    assert 'Item' in kwargs
    item_values = kwargs['Item'].values()
    assert len(item_values) == 4
    assert object_key in item_values
    assert geo.generate_geohash(coord) in item_values

    geo_json = kwargs['Item'][ddb.GEOJSON_ATTRIBUTE_NAME]
    assert isinstance(geo_json['coordinates'][0], decimal.Decimal)
    assert isinstance(geo_json['coordinates'][1], decimal.Decimal)
