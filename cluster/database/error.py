
# The errors for database acces

from flask import current_app, abort


class Bad_tsv_header(Exception):
    pass
class Not_found(Exception):
    pass
class Parent_not_found(Exception):
    pass
class Parent_not_supplied(Exception):
    pass


def abort_query(code, message):
    if current_app.config['TESTING']:
        return ({ 'status_code': code, 'message': message })
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
        400, 'There are children that would be orphaned, delete them first')


def abort_keyError(e):
    return abort_query(400, 'Database: invalid field: ' + str(e))


def abort_not_found(e):
    return abort_query(404, 'Not found: ' + str(e))


def abort_parent_not_found(e):
    return abort_query(404, 'Parent not found: ' + str(e))


def abort_parent_not_supplied(e):
    return abort_query(400, 'Parent was not supplied: ' + str(e))

