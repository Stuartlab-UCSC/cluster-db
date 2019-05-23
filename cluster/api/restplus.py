import logging
from flask_restplus import Api

log = logging.getLogger(__name__)
api = Api(version='0.1.0', title='Cluster Database API')
mimetype = 'text/plain'


# Default error handler.
@api.errorhandler
def default_error_handler(e):
    message = 'Error: ' + str(e)
    log.exception(message)
    return {'message': message}, 500


# Only needed to put the 'text-tsv' response content-type
# option in the drop-down on the swagger page.
@api.representation('text-tsv')
def tsv_response(data, code, headers=None):
       resp = app.make_response(data)
       resp.headers['Content-Type'] = 'application/json'
       return resp
