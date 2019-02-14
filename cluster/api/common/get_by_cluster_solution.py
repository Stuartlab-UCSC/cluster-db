
from flask import request, Response
from flask_restplus import Resource
from cluster.api.restplus import mimetype


# Get rows by cluster_solution.
@ns.route('/get_by' + \
    '/cluster_solution/<string:cluster_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('cluster_solution', 'cluster_solution name')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in TSV format')
    def get(self, cluster_solution, dataset):
        '''GET BY CLUSTER SOLUTION'''
        if table_name == 'attribute' or table_name == 'cell_assignment':
            resp = table.get_by_cluster_solution_clusters(
                [cluster_solution, dataset])
        else:
            resp = table.get_by_parent([cluster_solution, dataset])
        print('Get_by_parent:resp:',resp)
        return Response(str(resp), mimetype=mimetype)

