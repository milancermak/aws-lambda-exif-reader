import io
import os

def file_as_buffer(file_name):
    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(here, file_name)
    with open(path, 'rb') as f:
        buffer = io.BytesIO()
        buffer.write(f.read())
        return buffer
