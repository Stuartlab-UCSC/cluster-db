
# api/attribute.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api

table_name = 'attribute'
ns = api.namespace('attribute')
model = api.model('attribute', {
    'name': fields.String(required=True, description='sample name'),
    'value': fields.String(required=True, description='value for this sample'),
    'cluster': fields.String(required=True, description='cluster name'),
})
