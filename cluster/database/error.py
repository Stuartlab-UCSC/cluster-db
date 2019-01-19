
# The errors for database acces

from flask import current_app, abort


class Bad_tsv_header(Exception):
    pass
class Not_found(Exception):
    pass
class Updates_not_allowed(Exception):
    pass


def abort_query(code, message):
    if current_app.config['TESTING']:
        # NOTE: response.status_code is always 200 when testing because using
        # flask's abort() causes an exception within an exception. Tests
        # need to check the json or data of the response.
        return(str(code) + ' ' + message)
    else:
        abort(code, message)


def abort_bad_tsv_header(e):
    return abort_query(400, 'Bad TSV header:\n' + str(e))


def abort_database(e):
    message = str(e)
    if 'Incorrect number of bindings supplied' in message:
        message = 'Wrong number of columns supplied for add: ' + message
    return abort_query(400, 'Database: ' + message)


def abort_has_children():
    return abort_query(
        400, 'There are children that would be orphaned, delete those first')


def abort_keyError(e):
    return abort_query(400, 'Database: invalid field: ' + str(e))


def abort_not_found(e):
    return abort_query(404, 'Not found: ' + str(e))


def updates_not_allowed(e):
    return abort_query(400,
        'Updates to the database are not allowed, only read queries.')
