
# api/cluster.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database_update.cluster_table import cluster as table

table_name = 'cluster'
ns = api.namespace('cluster_update')
model = api.model('cluster', {
    'name': fields.String(required=True, description='Cluster name'),
    'cluster_solution': fields.String(
        required=True, description='Name of the cluster solution'),
})


# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "cluster/api_update/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = \
    "cluster/api_update/common/add_tsv_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = \
    "cluster/api_update/common/get_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/delete_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
