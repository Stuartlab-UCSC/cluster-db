
# api/baseRoute.py
# Common functions of APIs.

from werkzeug.exceptions import abort
from cluster.api.restplus import isTsv, abortIfTsv


def getAll(table):

    '''Get all'''
    if isTsv():
        return table.getTsv()
    return table.get()


def post(table, data):

    '''Add a new one'''
    abortIfTsv()
    return table.add(data)


def getOne(table, name):

    '''Get one by name'''
    abortIfTsv()
    row = table.get(name)
    if row is None:
        abort(404, 'Name not found: ' + str(name))
    return row


def delete(table, name):

    '''Delete one by name'''
    abortIfTsv()
    id = table.delete(name)
    if id is None:
        abort(404, 'Name not found: ' + str(name))
    return id


def put(table, name, data):

    '''Replace one by name'''
    abortIfTsv()
    id = table.replace(name, data)
    if id is None:
        abort(404, 'Name not found: ' + str(name))
    return id
