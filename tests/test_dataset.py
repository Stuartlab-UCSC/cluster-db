
import pytest
from cluster.database.db import get_db


#def test_index(client ''', auth'''):
def test_index(client):
    #response = client.get('/')
    #assert b"Log In" in response.data
    #assert b"Register" in response.data

    #auth.login()
    response = client.get('/')
    #assert b'Log Out' in response.data
    assert b'api' in response.data


# TODO
"""
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'
"""

"""
def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data
"""


# TODO
@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
#def test_exists_required(client, '''auth,''' path):
def test_exists_required(client, path):


#auth.login()
    assert client.post(path).status_code == 404


#def test_create(client, '''auth,''' app):
def test_create(client, app):
    #auth.login()
    # TODO
    response = client.get('/test')
    print('response.data:', response.data)
    print('response.location', response.location)
    assert response.status_code == 200

    response = client.get('/')
    print('response.data:', response.data)
    print('response.location', response.location)
    assert response.status_code == 302

    response = client.get('/api')
    print('response.data:', response.data)
    print('response.location', response.location)
    #assert response.status_code == 200

    response = client.get('/api/dataset')
    print('response.data:', response.data)
    print('response.location', response.location)
    assert response.status_code == 200

    client.post('/create', data={'name': 'dataset1', 'species': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM dataset').fetchone()[0]
        assert count == 2


