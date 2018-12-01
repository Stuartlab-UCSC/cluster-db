
# dataset/routes.py

from flask_restplus import Resource, fields
from cluster.api.restplus import api

ns = api.namespace('dataset', description='operations')


model = api.model('Dataset', {
    'id': fields.Integer(readOnly=True, description='The unique identifier'),
    'dataset': fields.String(required=True, description='The details')
})


class DatasetDAO(object):
    def __init__(self):
        self.counter = 0
        self.datasets = []

    def get(self, id):
        for dataset in self.datasets:
            if dataset['id'] == id:
                return dataset
        api.abort(404, "Dataset {} doesn't exist".format(id))

    def create(self, data):
        dataset = data
        dataset['id'] = self.counter = self.counter + 1
        self.datasets.append(dataset)
        return dataset

    def update(self, id, data):
        dataset = self.get(id)
        dataset.update(data)
        return dataset

    def delete(self, id):
        dataset = self.get(id)
        self.datasets.remove(dataset)


DAO = DatasetDAO()
DAO.create({'dataset': 'Build an API'})
DAO.create({'dataset': '?????'})
DAO.create({'dataset': 'profit!'})


def rowToTsv(row):
    return str(row['id']) + '\t' + row['dataset']


def rowsToTsv(rows):
    tsv = rowToTsv(rows[0])
    for row in rows[1:]:
        tsv += '\n' + rowToTsv(row)
    return tsv


@ns.route('/')
class DatasetList(Resource):
    '''Get a list of all, or add a new one'''

    @ns.doc('list_all')
    def get(self):
        '''List all'''
        return rowsToTsv(DAO.datasets)
        #return datasetTable.getAll()
    '''
    def getAll():
    data = cellDataset.getAll(appCtx)
    raise SuccessResp(data)
    '''

    @ns.doc('create_one')
    @ns.expect(model)
    @ns.marshal_with(model, code=201)
    def post(self):
        '''Add a new one'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Not found')
@ns.param('id', 'The identifier')
class Dataset(Resource):
    '''Get, update or delete one'''

    @ns.doc('get_one')
    @ns.marshal_with(model)
    def get(self, id):
        '''Get one given its ID'''
        return DAO.get(id)

    @ns.doc('delete_one')
    @ns.response(204, 'Object deleted')
    def delete(self, id):
        '''Delete one given its ID'''
        DAO.delete(id)
        return '', 204

    @ns.expect(model)
    @ns.marshal_with(model)
    def put(self, id):
        '''Update one given its ID'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
