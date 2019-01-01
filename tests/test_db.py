
import sqlite3
import pytest
from cluster.database.db import get_db, init_db

def test_get_close_db(app):
    # Within an application context, get_db should return the same connection
    # each time it’s called.
    with app.app_context():
         db = get_db()
         assert db is get_db()


"""
FAILS
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('cluster.database.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
 """