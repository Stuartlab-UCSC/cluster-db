
# api/cluster.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.cluster_table import cluster as table

table_name = 'cluster'
ns = api.namespace('cluster')
model = api.model('cluster', {
    'name': fields.String(required=True, description='Cluster name'),
    'clustering_solution': fields.String(
        required=True, description='Name of the clustering solution'),
})


# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "cluster/api/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = \
    "cluster/api/common/add_tsv_by_clustering_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = \
    "cluster/api/common/get_by_clustering_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api/common/delete_by_clustering_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
