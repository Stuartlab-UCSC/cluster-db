
# api/cluster.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api

table_name = 'cluster'
ns = api.namespace('cluster')
model = api.model('cluster', {
    'name': fields.String(required=True, description='Cluster name'),
    'cluster_solution': fields.String(
        required=True, description='Name of the cluster solution'),
})

