
# api/signature_gene_set.py

from flask_restplus import fields
from cluster.api.restplus import api
from cluster.database.dataset_table import dataset as table

ns = api.namespace('signature_gene_set')
model = api.model('signature_gene_set', {
    'name': fields.String(required=True, description='Gene set name'),
    'method': fields.String(required=True, description='Method used to determine this gene set'),
    'clustering': fields.String(required=True, description='Name of the clustering solution'),
})

# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/base_source.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
