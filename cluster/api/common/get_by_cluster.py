
from flask import Response
from flask_restplus import Resource
from cluster.api.restplus import api, mimetype

# Get rows by cluster.
@ns.route('/get_by' + \
    '/cluster/<string:cluster>' + \
    '/cluster_solution/<string:cluster_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('cluster_solution', 'cluster_solution name')
@ns.param('cluster', 'cluster name')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in TSV format')
    def get(self, cluster, cluster_solution, dataset):
        '''GET BY CLUSTER'''
        resp = table.get_by_parent([cluster, cluster_solution, dataset])
        return Response(str(resp), mimetype=mimetype)
