
# api/dataset.py

from flask import current_app, Response
from flask_restplus import fields, Resource
from cluster.api.restplus import api, mimetype
from cluster.database.dataset_table import dataset as table

table_name = 'dataset'
ns = api.namespace('dataset_update')
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

# Add from TSV file.
@ns.route('/add/tsv_file/<string:tsv_file>')
@ns.param('tsv_file', 'TSV file name')
class Add_tsv(Resource):
    @ns.response(200, 'last database row ID added')
    def get(self, tsv_file):
        '''ADD MANY FROM TSV FILE'''
        resp = table.add_tsv(tsv_file)
        print('Add__tsv:resp:', resp)
        return Response(str(resp), mimetype=mimetype)


# Do the equivalent of a bash shell 'source' to include the routes.
filename = "cluster/api_update/common/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/delete_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/get_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
