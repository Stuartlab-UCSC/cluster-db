
# api/dataset.py

from flask import request
from flask_restplus import Resource, fields
from werkzeug.exceptions import abort
from cluster.api.restplus import api
from cluster.database.datasetDb import dataset as table

ns = api.namespace('dataset', description='operations')

model = api.model('Dataset', {
    'id': fields.Integer(readOnly=True, description='The unique identifier'),
    'detail': fields.String(required=True, description='The details')
})

tsvUnsupported = 'TSV IS ONLY SUPPORTED FOR MULTI-ROW QUERIES'
#tsvUnsupported = {'message': 'TSV is only supported for multi-row queries'}


def isTsv():
    return request.headers['accept'] == 'text/tsv'


def abortIfTsv():
    if isTsv():
        abort(400, tsvUnsupported)


@ns.route('/')
class DatasetList(Resource):

    '''Get a list of all, or add a new one'''

    @ns.doc('list_all')
    #$@ns.marshal_list_with(model)
    def get(self):

        '''Get all'''
        if isTsv():
            return table.getTsv()
        return table.get()

    @ns.doc('create_one')
    @ns.expect(model)
    @ns.marshal_with(model, code=201)
    def post(self):

        '''Add a new one'''
        abortIfTsv()
        row = table.add(api.payload)
        if row is None:
            abort(400, 'add failed')
        return row, 201


@ns.route('/<int:id>')
@ns.response(404, 'Not found')
@ns.param('id', 'The identifier')
class Dataset(Resource):

    '''Get, update or delete one'''

    @ns.doc('get_one')
    @ns.marshal_with(model)
    def get(self, id):

        '''Get one given its ID'''
        abortIfTsv()
        row = table.get(id)
        if row is None:
            abort(404, 'ID ' + str(id) + ' does not exist.')
        return row

    @ns.doc('delete_one')
    @ns.response(204, 'Object deleted')
    def delete(self, id):

        '''Delete one given its ID'''
        abortIfTsv()
        table.delete(id)
        # TODO this is deleting and returning code 204, but no message
        return '', 204

    @ns.expect(model)
    @ns.marshal_with(model)
    def put(self, id):

        '''Update one given its ID'''
        abortIfTsv()
        row = table.update(id, api.payload)
        # TODO best way to pass more detailed error info?
        if row is None:
            abort(400, 'ID ' + str(id) + \
                ' failed to update. Maybe it does not exist.')
        return row


if __name__ == '__main__':
    app.run(debug=True)
