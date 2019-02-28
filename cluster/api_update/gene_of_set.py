
# api/gene_of_set.py

from flask import request, Response
from flask_restplus import fields,  Resource
from cluster.api.restplus import api, mimetype
from cluster.database_update.gene_of_set_table import gene_of_set as table

table_name = 'signature gene'
ns = api.namespace('gene-of-set-update')
model = api.model('gene_of_set', {
    'name': fields.String(required=True, description='Gene name'),
    'gene_set': fields.String(required=True, description='Name of the signature gene set'),
})


# Add from TSV file by gene_set.
@ns.route('/add' + \
    '/tsv_file/<string:tsv_file>' + \
    '/gene_set/<string:gene_set>' + \
    '/cluster_solution/<string:cluster_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('cluster_solution', 'cluster_solution name')
@ns.param('gene_set', 'gene_set name')
@ns.param('tsv_file', 'TSV file name')
class Add_many_tsv_file(Resource):
    @ns.response(200, 'last database row ID')
    def get(self, tsv_file, gene_set, cluster_solution, dataset):
        '''ADD MANY FROM TSV FILE'''
        resp = table.add_tsv(
            tsv_file, [gene_set, cluster_solution, dataset])
        return Response(str(resp), mimetype=mimetype)


# Get rows by gene_set.
@ns.route('/get_by' + \
    '/gene_set/<string:gene_set>' + \
    'cluster_solution/<string:cluster_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('cluster_solution', 'cluster_solution name')
@ns.param('gene_set', 'gene_set name')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in TSV format')
    def get(self, gene_set, cluster_solution, dataset):
        '''GET BY SIGNATURE GENE SET'''
        resp = table.get_by_parent(
            [gene_set, cluster_solution, dataset])
        return Response(str(resp), mimetype=mimetype)


# Delete by gene_set.
@ns.route('/delete_by' + \
    '/gene_set/<string:gene_set>' + \
    '/cluster_solution/<string:cluster_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('cluster_solution', 'cluster_solution name')
@ns.param('gene_set', 'gene_set name')
class Delete_by_cluster_solution(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, gene_set, cluster_solution, dataset):
        '''DELETE BY SIGNATURE GENE SET'''
        resp = table.delete_by_parent(
            [gene_set, cluster_solution, dataset])
        return Response(str(resp), mimetype=mimetype)

# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "cluster/api_update/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
