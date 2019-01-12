
# api/signature_gene.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.signature_gene_table import signature_gene as table

table_name = 'signature gene'
ns = api.namespace('signature_gene')
model = api.model('signature_gene', {
    'name': fields.String(required=True, description='Gene name'),
    'signature_gene_set': fields.String(required=True, description='Name of the signature gene set'),
})


# Add from TSV file by signature_gene_set.
@ns.route('/add' + \
    '/tsv_file/<string:tsv_file>' + \
    '/signature_gene_set/<string:signature_gene_set>' + \
    '/clustering_solution/<string:clustering_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('clustering_solution', 'clustering_solution name')
@ns.param('signature_gene_set', 'signature_gene_set name')
@ns.param('tsv_file', 'TSV file name')
class Add_many_tsv_file(Resource):
    @ns.response(200, 'Success')
    def get(self, tsv_file, signature_gene_set, clustering_solution, dataset):
        '''ADD MANY FROM TSV FILE'''
        return table.add_tsv(
            tsv_file, [signature_gene_set, clustering_solution, dataset])


# Get rows by signature_gene_set.
@ns.route('/get_by' + \
    '/signature_gene_set/<string:signature_gene_set>' + \
    'clustering_solution/<string:clustering_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('clustering_solution', 'clustering_solution name')
@ns.param('signature_gene_set', 'signature_gene_set name')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in JSON or TSV format')
    def get(self, signature_gene_set, clustering_solution, dataset):
        '''GET BY SIGNATURE GENE SET'''
        return table.get_by_parent(
            [signature_gene_set, clustering_solution, dataset],
            request.accept_mimetypes)

"""
# Delete by signature_gene_set.
@ns.route('/delete_by' + \
    '/signature_gene_set/<string:signature_gene_set>' + \
    '/clustering_solution/<string:clustering_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('clustering_solution', 'clustering_solution name')
@ns.param('signature_gene_set', 'signature_gene_set name')
class Delete_by_clustering_solution(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, dataset, clustering_solution, signature_gene_set):
        '''DELETE BY CLUSTERING_SOLUTION'''
        return table.delete_by_clustering_solution(
            dataset, clustering_solution, signature_gene_set)
"""
            
# Do the equivalent of a bash shell 'source' to get the base routes.
"""
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
"""