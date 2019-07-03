# content of conftest.py



import pytest

TEST_USER="test@test.com"

from tests.settings import TMPDIR

url_genss = [
        ("api.user_worksheet", {"user": "test@test.com", "worksheet": "test"}),
        ("api.user_gene_table", {"user": "test@test.com", "worksheet": "test", "cluster_name": "4"}),
        ("api.user_cluster_scatterplot", {"user": "test@test.com", "worksheet": "test", "type": "umap"}),
        ("api.user_gene_scatterplot", {"user": "test@test.com", "worksheet": "test", "type": "umap", "gene":"CC14"}),
    ]

@pytest.fixture(params=url_genss)
def url_gens(request):
    yield request.param



from cluster.app import create_app
from cluster.database import db as the_db

# Initialize the Flask-App with test-specific settings
the_app = create_app(dict(
    SQLALCHEMY_DATABASE_URI="sqlite://",
    SQLALCHEMY_USER_DATABASE_URI="sqlite://",
    TESTING=True,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    USER_EMAIL_SENDER_EMAIL="test@tests.com",
    USER_ENABLE_USERNAME=False,  # email auth only, no username is used
    USER_APP_NAME="UCSC Cell Atlas",  # in and email templates and page footers
    USER_AUTO_LOGIN=False,
    USER_AUTO_LOGIN_AFTER_REGISTER=False,
    USER_AUTO_LOGIN_AT_LOGIN=False,
    SECRET_KEY="*** super duper secret test password ***",
    WTF_CSRF_ENABLED=False,
    LOGIN_DISABLED=False,
    MAIL_SUPPRESS_SEND=True,
    SERVER_NAME="localhost.localdomain",

))

# Setup an application context (since the tests run outside of the webserver context)
the_app.app_context().push()

@pytest.fixture(scope='session')
def app():
    """ Makes the 'app' parameter available to test functions. """
    return the_app


@pytest.fixture(scope='session')
def db():
    """ Makes the 'db' parameter available to test functions. """
    return the_db

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

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

import shutil
import os
from tests.gen_data import write_all
@pytest.fixture(scope='session')
def user_worksheet_data(request, tmpdir=TMPDIR):
    os.mkdir(tmpdir)
    filepaths = write_all(tmpdir)
    def teardown():
        shutil.rmtree(tmpdir)

    request.addfinalizer(teardown)
    return filepaths


@pytest.fixture(scope='function')
def this_runs(tmp_path):
    print(tmp_path)

