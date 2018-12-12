
# api/clustering_solution.py

from flask_restplus import fields
from cluster.api.restplus import api
from cluster.database.clustering_solution_table import clustering_solution as table

ns = api.namespace('clustering_solution')
model = api.model('clustering_solution', {
    'name': fields.String(required=True, description='Unique clustering solution name'),
    'method': fields.String(required=True, description='Clustering method applied'),
    'method_implementation': fields.String(required=True, description='Clustering method implementation'),
    'method_url': fields.String(required=True, description='URL of clustering solution method'),
    'method_parameters': fields.String(required=True, description='Clustering method parameters'),
    'analyst': fields.String(required=True, description='Person who ran the analysis'),
    'secondary': fields.Integer(required=True,
        description='One means this is a secondary clustering solution and another clustering solution is the default'),
    'dataset': fields.String(required=True, description='Name of dataset that was analyzed'),
})
model_tsv_load = api.model('Clustering Solution TSV', {
    'url': fields.String(required=True, description='URL of the filename to load into the database'),
})

# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/base_source.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
