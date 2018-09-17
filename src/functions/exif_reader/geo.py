import collections

import s2sphere


Coordinate = collections.namedtuple('Coordinate', ('lat', 'lng'))


# pylint: disable=inconsistent-return-statements
def extract_coordinate(exif_data):
    if ('EXIF:GPSLatitude' in exif_data and 'EXIF:GPSLongitude' in exif_data):
        lat = exif_data['EXIF:GPSLatitude']
        lng = exif_data['EXIF:GPSLongitude']
        return Coordinate(lat, lng)

def generate_geohash(coord):
    # adapted from the dynamodb-geo lib
    # src/com/amazonaws/geo/s2/internal/S2Manager.java
    lat_lng = s2sphere.LatLng.from_degrees(coord.lat, coord.lng)
    cell_id = s2sphere.CellId.from_lat_lng(lat_lng)
    return cell_id.id()
