
from flask import request
from flask_restplus import Resource


# Get rows by clustering_solution.
@ns.route('/get_by' + \
    'clustering_solution/<string:clustering_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'name of parent dataset')
@ns.param('clustering_solution', 'name of parent clustering_solution')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in JSON or TSV format')
    def get(self, clustering_solution, dataset):
        '''GET BY CLUSTERING SOLUTION'''
        return table.get_by_parent([clustering_solution, dataset], request.accept_mimetypes)

