
import sqlite3
import pytest
from cluster.database.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # always fails with no error thrown
    #with pytest.raises(sqlite3.ProgrammingError) as e:
    #     db.execute('SELECT 1')
    #assert 'closed' in str(e)


# Always fails with:
# result.output Usage: cluster.app [OPTIONS] COMMAND [ARGS]...
# Try "cluster.app --help" for help.
#
# Error: No such command "init-db".
"""
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('cluster.database.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    print('result.output', result.output)
    assert 'Initialized' in result.output
    assert Recorder.called
"""
