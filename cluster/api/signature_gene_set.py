
# api/signature_gene_set.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.signature_gene_set_table import signature_gene_set as table

table_name = 'signature gene set'
ns = api.namespace('signature_gene_set')
model = api.model('signature_gene_set', {
    'name': fields.String(required=True, description='Gene set name'),
    'method': fields.String(required=True, description='Method used to determine this gene set'),
    'clustering_solution': fields.String(required=True, description='Name of the clustering solution'),
})

# Just debugging:
#filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_all.py"
#exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

# Do the equivalent of a bash shell 'source' to get the base routes.
filename = \
    "/Users/swat/dev/cdb/clusterDb/cluster/api/common/add_one_by_dataset.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = \
    "/Users/swat/dev/cdb/clusterDb/cluster/api/common/add_tsv_by_clustering_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = \
    "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_by_clustering_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
"""
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/delete.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
"""
