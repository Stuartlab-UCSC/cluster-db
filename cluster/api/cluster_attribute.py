
# api/cluster_attribute.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api

table_name = 'cluster_attribute'
ns = api.namespace('cluster-attribute-update')
model = api.model('cluster_attribute', {
    'name': fields.String(required=True, description='sample name'),
    'value': fields.String(required=True, description='value for this sample'),
    'cluster': fields.String(required=True, description='cluster name'),
})
