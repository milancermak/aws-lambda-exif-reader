import os
import sys

# to get current-path imports working when running tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..', '..', '..',
                                                'src', 'functions', 'exif_reader')))
