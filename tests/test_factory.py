
import os
from cluster.app import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True, 'DATABASE': 'fakeDb'}).testing
    os.remove('fakeDb')


def test_test(client):  # where second 'test' is the route
    response = client.get('/test')
    assert response.data == b'Just testing the clusterDb server'

