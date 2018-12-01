import logging
import traceback

from flask_restplus import Api
from cluster import settings

log = logging.getLogger(__name__)

api = Api(version='0.1.0', title='Cluster Database API')
          #description='A simple demonstration of a Flask RestPlus powered API')


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
