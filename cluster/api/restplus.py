import logging
import traceback
from flask import request
from flask_restplus import Api, fields
from werkzeug.exceptions import abort
from cluster import settings

log = logging.getLogger(__name__)

api = Api(version='0.1.0', title='Cluster Database API')
app = None

modelId = api.model('ID model', {
    'id': fields.Integer(readOnly=True, description='The unique identifier'),
})

modelRowCount = api.model('Row Count', {
    'row-count': fields.String(description='Number of rows'),
})

tsvUnsupported = 'TSV IS ONLY SUPPORTED FOR MULTI-ROW QUERIES'
JsonUnsupported = 'JSON IS ONLY SUPPORTED FOR SINGLE-ROW QUERIES'


def isTsv():
    return request.headers['accept'] == 'text/tsv'


def isJson():
    return request.headers['accept'] == 'application/json'


def abortIfJson():
    if isJson():
        abort(400, jsonUnsupported)


def abortIfTsv():
    if isTsv():
        abort(400, tsvUnsupported)


def NoResultFound(e):
    return 'exception: warning of no result found'


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 400


@api.representation('text/tsv')
def tsv_response(data, code, headers=None):
    resp = app.make_response(data)
    resp.headers['Content-Type'] = 'text/tsv'
    return resp


def init(flask_app):
    global app
    app = flask_app
