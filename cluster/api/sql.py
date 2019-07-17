
# api/query.py
from flask import Response, current_app, abort
from flask_restplus import Resource
from cluster.api.restplus import api, mimetype
import sqlite3
from cluster.database import db

ns = api.namespace('sql')

@ns.route('/<string:sql>')
@ns.param('sql', 'SQL read-only query string')
class List(Resource):
    @ns.response(200, 'Result of query')
    def get(self, sql):
        '''Generic read-only queries using raw sql.'''
        resp = query(sql)
        return Response(str(resp), mimetype=mimetype)


def database_query(query):
    try:
        # Don't allow updates to the database, only reads.
        lq = query.lower()
        if 'alter' in lq \
            or 'commit' in lq \
            or 'create' in lq \
            or 'delete' in lq \
            or 'drop' in lq \
            or 'insert' in lq \
            or 'reindex' in lq \
            or 'repace' in lq \
            or 'rollback' in lq \
            or 'update' in lq \
            or 'upsert' in lq \
            or 'user' in lq \
            or 'role' in lq \
            or 'worksheet' in lq \
            :
            raise UpdatesNotAllowed
        cursor = db.get_engine().execute(query)
        return from_rows(cursor.fetchall())

    except UpdatesNotAllowed as e:
        return updates_not_allowed(e)
    except NotFound as e:
        return abort_not_found(e)
    except sqlite3.IntegrityError as e:
        return abort_database(e)
    except sqlite3.ProgrammingError as e:
        return abort_database(e)
    except sqlite3.OperationalError as e:
        return abort_database(e)


def from_rows(rows):
    # Convert sqlite rows to TSV lines.
    if len(rows) < 1:
        return ''
    tsv = '\t'.join(rows[0].keys()) # the header
    for row in rows:
        lines = []
        for l in list(row.values()):
            lines.append(str(l))
        tsv += '\n' + '\t'.join(lines)
    return tsv


class BadTsvHeader(Exception):
    pass


class NotFound(Exception):
    pass


class UpdatesNotAllowed(Exception):
    pass


def abort_query(code, message):
    if current_app.config['TESTING']:
        # NOTE: response.status_code is always 200 when testing because using
        # flask's abort() causes an exception within an exception. Tests
        # need to check the json or data of the response.
        return(str(code) + ' ' + message)
    else:
        abort(code, message)


def abort_bad_tsv_header(e):
    return abort_query(400, 'Bad TSV header:\n' + str(e))


def abort_database(e):
    message = str(e)
    if 'Incorrect number of bindings supplied' in message:
        message = 'Wrong number of columns supplied for add: ' + message
    return abort_query(400, 'Database: ' + message)


def abort_has_children():
    return abort_query(
        400, 'There are children that would be orphaned, delete those first')


def abort_keyError(e):
    return abort_query(400, 'Database: invalid field: ' + str(e))


def abort_not_found(e):
    return abort_query(404, 'Not found: ' + str(e))


def updates_not_allowed(e):
    return abort_query(400,
        'Updates to the database are not allowed, only read queries.')