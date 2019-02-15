
# api/signature_gene_set.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api

table_name = 'signature gene set'
ns = api.namespace('signature_gene_set')
model = api.model('signature_gene_set', {
    'name': fields.String(required=True, description='Gene set name'),
    'method': fields.String(required=True, description='Method used to determine this gene set'),
    'cluster_solution': fields.String(required=True, description='Name of the cluster solution'),
})

