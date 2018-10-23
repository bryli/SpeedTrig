import os
import tempfile

import pytest
import SpeedTrig

@pytest.fixture
def client():
    SpeedTrig.app.config
    SpeedTrig.app.config['TESTING'] = True

