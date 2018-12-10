
# api/signature_gene.py

from flask_restplus import fields
from cluster.api.restplus import api
from cluster.database.datasetTable import dataset as table

ns = api.namespace('signature_gene')
model = api.model('signature_gene', {
    'name': fields.String(required=True, description='Gene name'),
    'signature_gene_set': fields.String(required=True, description='Name of signature gene set'),
    'id': fields.Integer(description='Unique identifier assigned by the database')
})

# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/base_source.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
