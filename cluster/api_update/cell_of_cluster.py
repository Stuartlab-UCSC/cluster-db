
# api/cell_of_cluster.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database_update.cell_of_cluster_table \
    import cell_of_cluster as table

table_name = 'cell_of_cluster'
ns = api.namespace('cell-of-cluster-update')
model = api.model('cell_of_cluster', {
    'name': fields.String(required=True, description='Sample name'),
    'cluster': fields.String(required=True, description='Name of the cluster'),
})

filename = "cluster/api_update/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/add_tsv_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/get_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/delete_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
