import logging
import traceback

from flask_restplus import Api
from cluster import settings

log = logging.getLogger(__name__)

api = Api(version='0.1.0', title='Cluster Database API')
app = None


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
    return {'message': 'A database result was required but none was found.'}, 40


@api.representation('text/tsv')
def tsv_response(data, code, headers=None):
    resp = app.make_response(data)
    resp.headers['Content-Type'] = 'text/tsv'
    return resp


def init(flask_app):
    global app
    app = flask_app
