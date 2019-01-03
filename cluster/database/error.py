
# The errors for database acces

from flask import current_app, abort


class Bad_tsv_header(Exception):
    pass
class Not_found(Exception):
    pass
class No_parent_row(Exception):
    pass
class No_parent_table(Exception):
    pass


def abort(code, message):
    if current_app.config['TESTING']:
        return ({ 'status_code': code, 'message': message })
    else:
        abort(code, message)

def abort_bad_tsv_header(e):
    return abort(400, 'Bad TSV header:\n' + str(e))


def abort_database(e):
    return abort(400, 'Database ' + str(e))


def abort_has_children():
    return ('There are children that would be orphaned, so this cannot be done')


def abort_keyError(e):
    return abort(400, 'Database invalid field: ' + str(e))


def abort_no_parent_row(e):
    return abort(404, 'Parent not found: ' + str(e))


def abort_no_parent_table(e):
    return abort(404, 'There is no parent table for ' + str(e) + 's')


def abort_not_found(e):
    return abort(404, 'Not found: ' + str(e))

