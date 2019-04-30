
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory

    g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def lists_equal(l1, l2):
    return ((l1 > l2) - (l1 < l2)) == 0


def dicts_equal(d1, d2):
    return lists_equal(list(d1.keys()), list(d2.keys())) and \
        lists_equal(list(d1.values()), list(d2.values()))


def merge_dicts(d1, d2):
    return {**d1, **d2}


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    init_db()

