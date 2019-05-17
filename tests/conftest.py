import os
import pytest

from cluster.app import create_app
from cluster.database import db as _db
from cluster.auth.db_models import User


CLUSTERDB = os.environ.get("CLUSTERDB")
TEST_DB_PATH = os.path.join(CLUSTERDB, 'clusterDb/tests/test.db')
#TEST_DB_URI = 'sqlite:///' + TEST_DB_PATH
TEST_USER_DB_PATH = os.path.join(CLUSTERDB, 'clusterDb/tests/testUser.db')
#TEST_USER_DB_URI = 'sqlite:///' + TEST_USER_DB_PATH


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'DEBUG': False,
        'SERVER_NAME': 'localhost.localdomain:5555',
        'SECRET_KEY': 'development_secret_key_for_testing',
        #'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'DATABASE': TEST_DB_PATH,
        'USER_DATABASE': TEST_USER_DB_PATH,
        'UPLOADS': os.path.join(CLUSTERDB, 'clusterDb/tests/uploads')
    }
    app = create_app(settings_override)

    # Establish an application context before running the tests.
    #ctx = app.app_context()
    ctx = app.test_request_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TEST_DB_PATH):
        os.unlink(TEST_DB_PATH)

    def teardown():
        _db.drop_all()
        if os.path.exists(TEST_DB_PATH):
            os.unlink(TEST_DB_PATH)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def with_admin_user(app, session, request):
    @app.login_manager.request_loader
    def load_user_from_request(request):
        # TODO only returns None:
        return session.query(User).first()
        #return db.session.query('User').first()
        #return db.query('User').first()

