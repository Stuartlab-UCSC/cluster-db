
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


# Add many from TSV file.
@ns.route('/add_many/tsv_file/<string:tsv_file>/clustering_solution/<string:clustering_solution_name>')
@ns.param('tsv_file', 'TSV file path')
@ns.param('clustering_solution_name', 'Clustering_solution these belong to')
class Add_many_tsv_file(Resource):
    @ns.response(200, 'Success with row count of added')
    def get(self, tsv_file, clustering_solution_name):
        '''ADD MANY FROM TSV FILE'''
        return table.add_many_tsv(tsv_file, clustering_solution_name)


# Get rows by parent (foreign key) name.
@ns.route('/get_by_clustering_solution/<string:clustering_solution_name>')
@ns.param('clustering_solution_name', 'name of parent clustering_solution')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in JSON or TSV format')
    def get(self, clustering_solution_name):
        '''GET BY CLUSTERING SOLUTION'''
        return table.get_by_parent(clustering_solution_name, request.accept_mimetypes)


# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/delete.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
