import os
import sys
import pytest

# manipulating sys.path to make importing of core work inside modules when running test
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'src'))


# runs automatically for every test
@pytest.fixture(autouse=True)
def setup_service_environment(monkeypatch):
    monkeypatch.setenv('REGION', os.uname().nodename)
    monkeypatch.setenv('SERVICE', 'strategy-bot')
    monkeypatch.setenv('STAGE', 'localtest')
