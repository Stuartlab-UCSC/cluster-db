
# api/gene_of_set.py

from flask import request, Response
from flask_restplus import fields,  Resource
from cluster.api.restplus import api, mimetype

table_name = 'signature gene'
ns = api.namespace('gene-of-set')
model = api.model('gene_of_set', {
    'name': fields.String(required=True, description='Gene name'),
    'gene_set': fields.String(required=True, description='Name of the signature gene set'),
})

