import logging
import traceback
from flask import request, abort
from flask_restplus import Api, fields

log = logging.getLogger(__name__)
api = Api(version='0.1.0', title='Cluster Database API')
mimetype = 'text/plain'

# Default error handler.
@api.errorhandler
def default_error_handler(e):
    message = 'Error: ' + str(e)
    log.exception(message)
    return {'message': message}, 500
