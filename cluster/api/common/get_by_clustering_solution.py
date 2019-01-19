
from flask import request, Response
from flask_restplus import Resource
from cluster.api.restplus import mimetype


# Get rows by clustering_solution.
@ns.route('/get_by' + \
    '/clustering_solution/<string:clustering_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('clustering_solution', 'clustering_solution name')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in TSV format')
    def get(self, clustering_solution, dataset):
        '''GET BY CLUSTERING SOLUTION'''
        if table_name == 'attribute' or table_name == 'cluster_assignment':
            resp = table.get_by_clustering_solution_clusters(
                [clustering_solution, dataset])
        else:
            resp = table.get_by_parent([clustering_solution, dataset])
        print('Get_by_parent:resp:',resp)
        return Response(str(resp), mimetype=mimetype)

