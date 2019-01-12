
from flask_restplus import Resource
from cluster.api.restplus import api

# Get rows by cluster.
@ns.route('/get_by' + \
    '/cluster/<string:cluster>' + \
    '/clustering_solution/<string:clustering_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('clustering_solution', 'clustering_solution name')
@ns.param('cluster', 'cluster name')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in JSON or TSV format')
    def get(self, cluster, clustering_solution, dataset):
        '''GET BY CLUSTER'''
        return table.get_by_parent([cluster, clustering_solution, dataset],
            request.accept_mimetypes)
