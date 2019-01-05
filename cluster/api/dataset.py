
# api/dataset.py

from flask_restplus import fields, Resource
from cluster.api.restplus import api
from cluster.database.dataset_table import dataset as table

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


# Add many from TSV file.
@ns.route('/add_many/tsv_file/<string:tsv_file>')
@ns.param('tsv_file', 'TSV file path')
class Add_many_tsv_file(Resource):
    @ns.response(200, 'Success')
    def get(self, tsv_file):
        '''ADD MANY FROM TSV FILE'''
        return table.add_many_tsv_file(tsv_file)


# Do the equivalent of a bash shell 'source' to include the routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/delete.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
