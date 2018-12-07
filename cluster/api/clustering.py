
# api/clustering.py

from flask_restplus import Resource, fields
from werkzeug.exceptions import abort
from cluster.api.restplus import modelId, isTsv, abortIfTsv
from cluster.api.restplus import api
from cluster.database.clusteringTable import clustering as table

ns = api.namespace('clustering', description='operations')

model = api.model('Clustering', {
    'name': fields.String(required=True, description='Unique clustering name'),
    'method': fields.String(description='Clustering method applied'),
    'method_url': fields.String(description='URL of clustering method'),
    'method_parameters': fields.String(description='Clustering method parameters'),
    'analyst': fields.String(description='Person who ran the analysis'),
    'secondary': fields.Boolean(description='True means this is a secondary clustering and another is the default'),
    'dataset': fields.Integer(description='Dataset upon which the analysis was performed'),
})

modelWithId = api.clone('Clustering with ID', model, {
    'id': fields.Integer(description='Unique identifier assigned by the database')
})

@ns.route('/')
class ClusteringList(Resource):

    '''Get a list of all, or add a new one'''

    @ns.response(200, 'list of all as JSON or TSV')
    def get(self):

        '''Get all'''
        if isTsv():
            return table.getTsv()
        return table.get(), 200

    @ns.expect(model)
    @ns.response(200, 'ID of added', modelId)
    def post(self):

        '''Add a new one'''
        abortIfTsv()
        return table.add(api.payload), 200


@ns.route('/<string:name>')
@ns.response(404, 'Not found')
@ns.param('name', 'The name')
class Clustering(Resource):

    '''Get, update or delete one'''

    @ns.marshal_with(modelWithId)
    def get(self, name):

        '''Get one by name'''
        abortIfTsv()
        row = table.get(name)
        if row is None:
            abort(404, name + ' does not exist.')
        return row

    @ns.response(200, 'Deleted one')
    def delete(self, name):

        '''Delete one by name'''
        abortIfTsv()
        table.delete(name)
        return 'Deleted one', 200
        # TODO implement not found response


if __name__ == '__main__':
    app.run(debug=True)
