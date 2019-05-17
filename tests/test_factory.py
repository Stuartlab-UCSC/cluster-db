
import os
from cluster.app import create_app


def test_test(client):  # where second 'test' is the route
    response = client.get('/test')
    assert response.data == b'Just testing the clusterDb server'

