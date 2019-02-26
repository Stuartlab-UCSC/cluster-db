import logging
import traceback
from flask import request, abort
from flask_restplus import Api, fields

log = logging.getLogger(__name__)
api = Api(version='0.1.1', title='Cluster Update API (admin privileges required)')
mimetype = 'text/plain'

# Default error handler.
@api.errorhandler
def default_error_handler(e):
    message = 'Error: ' + str(e)
    log.exception(message)
    return {'message': message}, 500
