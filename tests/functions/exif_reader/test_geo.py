import pytest

from functions.exif_reader import geo


def test_coordinate():
    coord = geo.Coordinate(1, 2)
    assert coord.lat == 1
    assert coord.lng == 2

extract_coordinate_fixture = [
    ({'EXIF:GPSLatitude': 8.142827,
      'EXIF:GPSLongitude': 79.7096861}, geo.Coordinate(8.142827, 79.7096861)),
    ({}, None)
]
@pytest.mark.parametrize('exif, expected', extract_coordinate_fixture)
def test_extract_coordinate(exif, expected):
    coord = geo.extract_coordinate(exif)
    assert coord == expected

def test_generate_geohash():
    coord = geo.Coordinate(-30.043800, -51.140220)
    cell_id = 10743750136202470315
    geohash = geo.generate_geohash(coord)
    assert geohash == cell_id
