import logging
import traceback
from flask import request, abort
from flask_restplus import Api, fields
from cluster import config  # TODO why settings.py and config.py?

log = logging.getLogger(__name__)
api = Api(version='0.1.0', title='Cluster Database API')
app = None


@api.errorhandler
def default_error_handler(e):
    message = 'Error: ' + str(e)
    log.exception(message)
    if not config.FLASK_DEBUG:
        return {'message': message}, 500


@api.representation('text/tsv')
def tsv_response(data, code, headers=None):
    resp = app.make_response(data)
    resp.headers['Content-Type'] = 'application/json'
    return resp


def init(flask_app):
    global app
    app = flask_app
