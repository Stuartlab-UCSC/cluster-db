
# api/query.py
# Generic read query in SGL
from flask import Response, current_app, abort
from flask_restplus import Resource
from cluster.api.restplus import api, mimetype
import sqlite3
from cluster.database import db
import cluster.database.error as err
from cluster.database.error import Not_found, Updates_not_allowed
import cluster.database.tsv as tsv

ns = api.namespace('sql')


@ns.route('/<string:sql>')
@ns.param('sql', 'SQL read-only query string')
class List(Resource):
    @ns.response(200, 'Result of query')
    def get(self, sql):
        '''Generic read-only queries using raw sql.'''
        resp = database_query(sql)
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
            :
            raise Updates_not_allowed
        cursor = db.get_engine().execute(query)
        return tsv.from_rows(cursor.fetchall())
    except Updates_not_allowed as e:
        return err.updates_not_allowed(e)
    except Not_found as e:
        return err.abort_not_found(e)
    except sqlite3.IntegrityError as e:
        return err.abort_database(e)
    except sqlite3.ProgrammingError as e:
        return err.abort_database(e)
    except sqlite3.OperationalError as e:
        return err.abort_database(e)


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


def abort_database(e):
    message = str(e)
    if 'Incorrect number of bindings supplied' in message:
        message = 'Wrong number of columns supplied for add: ' + message
    return abort_query(400, 'Database: ' + message)


def abort_query(code, message):
    if current_app.config['TESTING']:
        # NOTE: response.status_code is always 200 when testing because using
        # flask's abort() causes an exception within an exception. Tests
        # need to check the json or data of the response.
        return(str(code) + ' ' + message)
    else:
        abort(code, message)


