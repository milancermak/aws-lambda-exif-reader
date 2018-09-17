import io
import json
import os
import subprocess
import tempfile

import boto3


def fetch_from_bucket(bucket_name, object_key):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, object_key)

    buffer = io.BytesIO()
    obj.download_fileobj(buffer)
    buffer.seek(0)
    return buffer

def read_exif_from_image(buffer):
    buffer.seek(0)
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(buffer.read())
        tmp.seek(0)
        here = os.path.abspath(os.path.dirname(__file__))
        exiftool_path = os.path.join(here, 'exiftool')
        command = [exiftool_path, '-G', '-j', '-n', '-sort', tmp.name]
        p = subprocess.Popen(command, stdout=subprocess.PIPE)

        output = p.stdout.read().decode('utf-8')
        if output and 'ExifTool:Error' not in output:
            arr = json.loads(output)
            return arr[0]
