
# Handle database errors

import logging, traceback
from flask_restplus import abort

log = logging.getLogger(__name__)


def abort_400_trace(message):
    print ('abort_400_trace:message', message)
    trace = str(traceback.format_exc(100))
    log.error(message + '\n' + trace)
    abort(400, error=message, trace=trace)


class Bail_404(Exception):
    pass


def message_404(table, name):
    return('Not found: ' + table + ': ' + str(name))
