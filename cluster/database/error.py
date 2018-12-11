
# Handle database errors

import logging, traceback
from werkzeug.exceptions import abort

log = logging.getLogger(__name__)


def abort_400_trace(message):
    print ('abort_400_trace:message', message)
    message += '\n' + str(traceback.format_exc(100))
    log.error(message)
    abort(400, message)


