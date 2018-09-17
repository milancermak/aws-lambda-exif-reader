import io

def file_as_buffer(path):
    with open(path, 'rb') as f:
        buffer = io.BytesIO()
        buffer.write(f.read())
        return buffer
