
# api/cell_assignment.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.cell_assignment_table \
    import cell_assignment as table

table_name = 'cell_assignment'
ns = api.namespace('cell_assignment')
model = api.model('cell_assignment', {
    'name': fields.String(required=True, description='Sample name'),
    'cluster': fields.String(required=True, description='Name of the cluster'),
})

filename = "cluster/api/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api/common/add_tsv_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api/common/get_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api/common/delete_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
