
# api/dataset.py

from flask import current_app, Response
from flask_restplus import fields, Resource
from cluster.api.restplus import api, mimetype
from cluster.database_update.dataset_table import dataset as table

table_name = 'dataset'
ns = api.namespace('dataset')
model = api.model('dataset', {
    'name': fields.String(required=True, description='Unique dataset name'),
    'species': fields.String(required=True, description='Species studied')
})
"""
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
"""

# Get all
@ns.route('/')
class List(Resource):
    @ns.response(200, 'list of all ' + table_name + 's in TSV format')
    def get(self):
        '''GET ALL'''
        return Response(table.get_all(), mimetype=mimetype)
