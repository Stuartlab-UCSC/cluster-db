
# api/signature_gene.py

from flask import request, Response
from flask_restplus import fields,  Resource
from cluster.api.restplus import api, mimetype

table_name = 'signature gene'
ns = api.namespace('signature_gene')
model = api.model('signature_gene', {
    'name': fields.String(required=True, description='Gene name'),
    'signature_gene_set': fields.String(required=True, description='Name of the signature gene set'),
})

