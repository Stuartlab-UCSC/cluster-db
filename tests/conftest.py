
import os
import tempfile
import pytest
from cluster.app import create_app
from cluster.database.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture(scope="function")
def app():
    CLUSTERDB = os.environ.get("CLUSTERDB")
    db_fd, db_path = tempfile.mkstemp()
    uploads = os.path.join(CLUSTERDB, 'clusterDb/tests/uploads')

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'UPLOADS': uploads
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

