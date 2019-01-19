
from flask import Response
from flask_restplus import Resource, mimetype
from cluster.api.restplus import api

# Add from TSV file by cluster.
@ns.route('/add/tsv_file/<string:tsv_file>' + \
    '/cluster/<string:cluster>' + \
    '/clustering_solution/<string:clustering_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('clustering_solution', 'clustering_solution name')
@ns.param('cluster', 'cluster name')
@ns.param('tsv_file', 'TSV file name')
class Add_many_tsv_file(Resource):
    @ns.response(200, 'last database row ID added')
    def get(self, tsv_file, cluster, clustering_solution, dataset):
        '''ADD MANY FROM TSV FILE'''
        resp table.add_tsv(tsv_file, [cluster, clustering_solution, dataset])
        return Response(str(resp), mimetype=mimetype)

