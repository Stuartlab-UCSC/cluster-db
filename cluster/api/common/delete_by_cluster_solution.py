
from flask_restplus import Resource
from cluster.api.restplus import mimetype


# Delete many rows by cluster_solution.
@ns.route('/delete_by' + \
    '/cluster_solution/<string:cluster_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('cluster_solution', 'cluster_solution name')
class Delete_by_cluster_solution(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, cluster_solution, dataset):
        '''DELETE BY CLUSTERING_SOLUTION'''
        if table_name == 'attribute' or table_name == 'cell_assignment':
            resp = table.delete_by_cluster_solution_clusters(
                [cluster_solution, dataset])
        else:
            resp = table.delete_by_parent([cluster_solution, dataset])
        return Response(str(resp), mimetype=mimetype)
