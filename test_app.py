from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
import SpeedTrig

@pytest.fixture
def app():
    SpeedTrig.app.config['TESTING'] = True
    return SpeedTrig.app

def test_norm_reci(client):
    response = client.post('generated-quiz', data=dict(norm=True, reci=False, inc=False, Override=False, chance=40, num=2))
    assert response.status_code == 200

def test_out_range(client):
    response = client.post('generated-quiz', data=dict(norm=True, reci=True, inc=True, Override=False, chance=40, num=2))
    assert response.status_code == 200

def test_blank(client):
    response = client.post('generated-quiz', data={})
    assert response.status_code == 204

def test_outrange_blank(client):
    response = client.post('generated-quiz', data=dict(norm=True, reci=True))
    assert response.status_code == 200
