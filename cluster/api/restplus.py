import logging
import traceback
from flask import request
from flask_restplus import Api, fields
from werkzeug.exceptions import abort
from cluster import settings

log = logging.getLogger(__name__)

api = Api(version='0.1.0', title='Cluster Database API')
app = None

model_id = api.model('ID model', {
    'id': fields.Integer(readOnly=True, description='The unique identifier'),
})

model_row_count = api.model('Row Count', {
    'row-count': fields.String(description='Number of rows'),
})

tsv_unsupported = 'TSV IS ONLY SUPPORTED FOR MULTI-ROW QUERIES'
json_unsupported = 'JSON IS ONLY SUPPORTED FOR SINGLE-ROW QUERIES'


def is_tsv():
    return request.headers['accept'] == 'text/tsv'


def is_json():
    return request.headers['accept'] == 'application/json'


def abort_if_json():
    if is_json():
        abort(400, jsonUnsupported)


def abort_if_tsv():
    if is_tsv():
        abort(400, tsv_unsupported)


def no_result_found(e):
    return 'exception: warning of no result found'


@api.errorhandler
def default_error_handler(e):
    print('!!!!!!!!!!!! in default_error_handler() !!!!!!!!!!!!!')
    message = 'An unhandled exception occurred.'
    log.exception(message)
    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(bad_request)
def default_error_handler(e):
    print('!!!!!!!!!!!! in app_error_handler() !!!!!!!!!!!!!')
    message = 'An app exception occurred.'
    log.exception(message)
    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(no_result_found)
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
