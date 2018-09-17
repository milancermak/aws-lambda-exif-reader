import jmespath

from core import logger
from . import ddb, geo, utils


def handler(event, context):
    logger.info(event)
    object_key = jmespath.search('Records[0].s3.object.key', event)
    if not object_key:
        logger.error('No file found in invocation event')
        return
    bucket_name = jmespath.search('Records[0].s3.bucket.name', event)
    image_buffer = utils.fetch_from_bucket(bucket_name, object_key)
    exif_data = utils.read_exif_from_image(image_buffer)

    if not exif_data:
        logger.info('No EXIF data found in image')
        return

    logger.info('Writing EXIF data to database')
    ddb.store_exif_data(object_key, exif_data)

    coord = geo.extract_coordinate(exif_data)
    if coord:
        logger.info('Found geo coordinate, writing to geo table')
        ddb.store_coordinate(object_key, coord)
    else:
        logger.info('No geo coordinate found in EXIF data')
