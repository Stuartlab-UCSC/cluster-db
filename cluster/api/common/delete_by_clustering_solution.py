
from flask_restplus import Resource


# Delete by clustering_solution.
@ns.route('/delete_by' + \
    '/dataset/<string:dataset>' + \
    '/clustering_solution/<string:clustering_solution>')
@ns.param('dataset', 'name of dataset')
@ns.param('clustering_solution', 'name of clustering_solution')
class Delete_by_clustering_solution(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, clustering_solution, dataset):
        '''DELETE BY CLUSTERING_SOLUTION'''
        return table.delete_by_clustering_solution(clustering_solution, dataset)
