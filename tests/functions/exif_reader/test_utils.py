import io
import os
from unittest.mock import Mock

import pytest

from functions.exif_reader import utils
from helpers import file_as_buffer


def test_fetch_from_bucket(monkeypatch):
    mock_s3 = Mock()
    monkeypatch.setattr('boto3.resource', lambda *_args: mock_s3)
    mock_obj = Mock()
    mock_s3.Object.return_value = mock_obj
    bucket_name = 'foo'
    object_key = 'bar'

    buffer = utils.fetch_from_bucket(bucket_name, object_key)

    assert mock_s3.Object.call_count == 1
    assert mock_s3.Object.call_args[0] == (bucket_name, object_key)
    assert mock_obj.download_fileobj.call_count == 1
    assert mock_obj.download_fileobj.call_args[0] == (buffer,)
    assert isinstance(buffer, io.BytesIO)
    assert buffer.tell() == 0

@pytest.mark.parametrize('image_name', ('happydog.jpg', 'matterhorn.png'))
def test_read_exif_from_image(image_name):
    here = os.path.abspath(os.path.dirname(__file__))
    image_path = os.path.join(here, image_name)
    buffer = file_as_buffer(image_path)
    exif_data = utils.read_exif_from_image(buffer)

    assert isinstance(exif_data, dict)
    assert 'ExifTool:Error' not in exif_data

def test_read_exif_from_image_faux_input():
    this_path = os.path.abspath(__file__)
    buffer = file_as_buffer(this_path)
    exif_data = utils.read_exif_from_image(buffer)

    assert exif_data is None
