import decimal
import json
import math
import os

import boto3

import geo


HASHKEY_ATTRIBUTE_NAME = 'hashKey'
RANGEKEY_ATTRIBUTE_NAME = 'rangeKey'
GEOHASH_ATTRRIBUTE_NAME = 'geohash'
GEOJSON_ATTRIBUTE_NAME = 'geoJson'

dynamodb = boto3.resource('dynamodb')


def decimal_from_float(f):
    # from ://github.com/boto/boto3/issues/665#issuecomment-223851711
    with decimal.localcontext(boto3.dynamodb.types.DYNAMODB_CONTEXT) as ctx:
        ctx.traps[decimal.Inexact] = False
        ctx.traps[decimal.Rounded] = False
        return ctx.create_decimal_from_float(f)

def decimalize(data_dict):
    # pylint: disable=invalid-name

    d = {}
    for k, v in data_dict.items():
        if isinstance(v, float):
            d[k] = decimal_from_float(v)
        else:
            d[k] = v
    return d

def generate_hash_key(geohash, hash_key_length):
    # adapted from the dynamodb-geo lib
    # src/com/amazonaws/geo/s2/internal/S2Manager.java
    key_length = int(hash_key_length)
    if geohash < 0:
        key_length += 1
    denominator = math.pow(10, len(str(int(geohash))) - key_length)
    return int(geohash / denominator)

def store_exif_data(object_key, exif_data):
    table = dynamodb.Table(os.environ['EXIF_DATA_TABLE'])
    item = {HASHKEY_ATTRIBUTE_NAME: object_key,
            'exif_data': decimalize(exif_data)}
    table.put_item(Item=item)

def store_coordinate(object_key, coord):
    geohash = geo.generate_geohash(coord)
    hash_key = generate_hash_key(geohash, os.environ['HASH_KEY_LENGTH'])
    # GeoJSON RFC defines a Position as two elements of longitude and latitude
    # https://tools.ietf.org/html/rfc7946#section-3.1.1
    # however the dynamodb-geo library swaps the order...
    geo_json = json.dumps({'type': 'Point',
                           'coordinates': [coord.lng, coord.lat],
                           'object_key': object_key})

    table = dynamodb.Table(os.environ['GEO_DATA_TABLE'])
    item = {HASHKEY_ATTRIBUTE_NAME: hash_key,
            RANGEKEY_ATTRIBUTE_NAME: object_key,
            GEOHASH_ATTRRIBUTE_NAME: geohash,
            GEOJSON_ATTRIBUTE_NAME: geo_json}
    table.put_item(Item=item)
