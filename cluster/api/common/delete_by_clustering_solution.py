
from flask_restplus import Resource
from cluster.api.restplus import mimetype


# Delete many rows by clustering_solution.
@ns.route('/delete_by' + \
    '/clustering_solution/<string:clustering_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('clustering_solution', 'clustering_solution name')
class Delete_by_clustering_solution(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, clustering_solution, dataset):
        '''DELETE BY CLUSTERING_SOLUTION'''
        if table_name == 'attribute' or table_name == 'cluster_assignment':
            resp = table.delete_by_clustering_solution_clusters(
                [clustering_solution, dataset])
        else:
            resp = table.delete_by_parent([clustering_solution, dataset])
        return Response(str(resp), mimetype=mimetype)
