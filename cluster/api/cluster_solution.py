
# api/cluster_solution.py

from flask import request, Response
from flask_restplus import fields,  Resource
from cluster.api.restplus import api, mimetype
from cluster.database.cluster_solution_table import cluster_solution as table

table_name = 'cluster_solution'
ns = api.namespace('cluster_solution')
model = api.model('cluster_solution', {
    'name': fields.String(required=True, description='Unique cluster solution name'),
    'method': fields.String(required=True, description='Clustering method applied'),
    'method_implementation': fields.String(required=True, description='Clustering method implementation'),
    'method_url': fields.String(required=True, description='URL of clustering method'),
    'method_parameters': fields.String(required=True, description='Clustering method parameters'),
    'scores': fields.String(description='Scores for this cluster solution'),
    'analyst': fields.String(required=True, description='Person who ran the analysis'),
    'secondary': fields.Integer(required=True, \
        description='One means this is a secondary cluster solution and some other cluster solution is the default'),
    'dataset': fields.String(required=True, description='Name of dataset that was analyzed'),
})
