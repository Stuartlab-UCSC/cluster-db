
import os
import tempfile

import pytest
from flask import current_app, g

from cluster.app import create_app
from cluster.database.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    config = {
        'TESTING': True,
        'DATABASE': db_path
    }
    app = create_app(config)

    file = '/Users/swat/dev/cdb/clusterDB/cluster/database/schema.sql'
    with app.app_context():
        with app.open_resource(file) as f:
            get_db().executescript(f.read().decode('utf8'))

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
