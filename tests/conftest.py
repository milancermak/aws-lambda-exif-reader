import os
import sys

# manipulating sys.path to make importing of core work inside modules when running test
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'src'))
