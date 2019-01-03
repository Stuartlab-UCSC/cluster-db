
# api/dataset.py

from flask_restplus import fields
from cluster.api.restplus import api
from cluster.database.dataset_table import dataset as table

table_name = 'dataset'
ns = api.namespace('dataset')
model = api.model('dataset', {
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

# Do the equivalent of a bash shell 'source' to include the routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/delete.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/delete_with_children.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/get_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/load_tsv.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
