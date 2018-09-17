import os
import sys

# manipulating sys.path to make importing inside tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   '..', 'src'))) # for core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   '..', 'src', 'functions'))) # for functions
