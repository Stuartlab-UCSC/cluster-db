
# api/clustering_solution.py

from flask_restplus import fields
from cluster.api.restplus import api
from cluster.database.clustering_solution_table import clustering_solution as table

table_name = 'clustering solution'
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

# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/get_by_parent.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/delete.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

