
from cluster.app import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True, 'DATABASE': 'fakeDb'}).testing


def test_test(client):  # where second 'test' is the route
    response = client.get('/api')
    print('!!!!!!!!!!response.data:', response.data)
    print('!!!!!!!response.location', response.location)
    assert response.data == b'Just testing the clusterDb server'
