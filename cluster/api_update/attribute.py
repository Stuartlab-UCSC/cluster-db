
# api/attribute.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.attribute_table import attribute as table

table_name = 'attribute'
ns = api.namespace('attribute_update')
model = api.model('attribute', {
    'name': fields.String(required=True, description='sample name'),
    'value': fields.String(required=True, description='value for this sample'),
    'cluster': fields.String(required=True, description='cluster name'),
})

filename = "cluster/api_update/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/add_tsv_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/get_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/delete_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
