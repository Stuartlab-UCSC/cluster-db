
# api/signature_gene.py

from flask_restplus import fields
from cluster.api.restplus import api
from cluster.database.signature_gene_table import signature_gene as table

table_name = 'signature gene'
ns = api.namespace('signature_gene')
model = api.model('signature_gene', {
    'name': fields.String(required=True, description='Gene name'),
    'signature_gene_set': fields.String(required=True, description='Name of the signature gene set'),
})

# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/add_many_tsv.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/sourced/get_by_parent.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))


