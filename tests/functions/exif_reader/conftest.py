import os
import sys

# to get `import geo` in ddb.py working
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..', '..', '..',
                                                'src', 'functions', 'exif_reader')))
