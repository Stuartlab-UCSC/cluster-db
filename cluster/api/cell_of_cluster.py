
# api/cell_of_cluster.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api

table_name = 'cell_of_cluster'
ns = api.namespace('cell-of-cluster')
model = api.model('cell_of_cluster', {
    'name': fields.String(required=True, description='Sample name'),
    'cluster': fields.String(required=True, description='Name of the cluster'),
})

