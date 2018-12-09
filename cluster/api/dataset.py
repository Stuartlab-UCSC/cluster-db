
# api/dataset.py

from flask_restplus import Resource, fields
from cluster.api.restplus import api, modelId
from cluster.api.baseRoute import delete, getAll, getOne, post, put
from cluster.database.datasetTable import dataset as table

ns = api.namespace('dataset', description='operations')

model = api.model('Dataset', {
    'name': fields.String(required=True, description='Unique dataset name'),
    'species': fields.String(required=True, description='Species studied'),
    'organ': fields.String(description='source organ'),
    'sampleCount': fields.Integer(description='Count of samples in the dataset'),
    'abnormality': fields.String(description='Any abnormality of the dataset, i.e. cancer'),
    'primaryData': fields.String(description='location of initial data'),
    'scanpyObjectOfPrimaryData': fields.String(description='location of initial scanpy object'),
    'sampleMetadata': fields.String(description='Initial metadata of samples'),
    'primaryDataNormalizationStatus': fields.String(description='Normalization status of initial data'),
    'reasonableForTrajectoryAnalysis': fields.Boolean(description='Is suitable for trajectory analysis'),
    'platform': fields.String(description='Genomic sequencing platform'),
    'expressionDataSource': fields.String(description='Source of expression data'),
    'expressionDataSourceURL': fields.String(description='URL of expression source'),
})

modelWithId = api.clone('Dataset with ID', model, {
    'id': fields.Integer(description='Unique identifier assigned by the database')
})

modelTsv = api.model('Dataset TSV', {
    'url': fields.String(required=True, description='URL of the file to load into the database'),
    'replace': fields.Boolean(description='true to replace the entire table in the database'),
})


@ns.route('/')
class DatasetList(Resource):
    '''Get all, or add a new one'''

    @ns.response(200, 'list of all as JSON or TSV')
    def get(self):
        '''Get all'''
        return getAll(table)

    @ns.expect(model)
    @ns.response(200, 'ID of added', modelId)
    def post(self):
        '''Add a new one'''
        return post(table, api.payload)


@ns.route('/<string:name>')
@ns.response(404, 'Not found')
@ns.param('name', 'The name')
class Dataset(Resource):
    '''Get, update or delete one'''

    @ns.marshal_with(modelWithId)
    def get(self, name):
        '''Get one by name'''
        return getOne(table, name)

    @ns.marshal_with(modelId)
    @ns.response(200, 'ID of deleted', modelId)
    def delete(self, name):
        '''Delete one by name'''
        return delete(table, name)

    @ns.expect(model)
    @ns.marshal_with(modelId)
    @ns.response(200, 'ID of replaced', modelId)
    def put(self, name):
        '''Replace one by name'''
        return put(table, name, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
