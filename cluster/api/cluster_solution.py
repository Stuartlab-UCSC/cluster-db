
# api/cluster_solution.py

from flask import request, Response
from flask_restplus import fields,  Resource
from cluster.api.restplus import api, mimetype
from cluster.database.cluster_solution_table import cluster_solution as table

table_name = 'cluster_solution'
ns = api.namespace('cluster_solution')
model = api.model('cluster_solution', {
    'name': fields.String(required=True, description='Unique cluster solution name'),
    'method': fields.String(required=True, description='Clustering method applied'),
    'method_implementation': fields.String(required=True, description='Clustering method implementation'),
    'method_url': fields.String(required=True, description='URL of clustering method'),
    'method_parameters': fields.String(required=True, description='Clustering method parameters'),
    'scores': fields.String(description='Scores for this cluster solution'),
    'analyst': fields.String(required=True, description='Person who ran the analysis'),
    'secondary': fields.Integer(required=True, \
        description='One means this is a secondary cluster solution and some other cluster solution is the default'),
    'dataset': fields.String(required=True, description='Name of dataset that was analyzed'),
})


# Add from TSV file.
@ns.route('/add' + \
    '/tsv_file/<string:tsv_file>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('tsv_file', 'TSV file name')
class Add_tsv(Resource):
    @ns.response(200, 'database row ID')
    def get(self, tsv_file, dataset):
        '''ADD FROM TSV FILE BY CLUSTERING_SOLUTION'''
        resp = table.add_tsv(tsv_file, ['dataset1'])
        return Response(str(resp), mimetype=mimetype)


# Delete one.
@ns.route('/delete' + \
    '/<string:cluster_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('cluster_solution', 'cluster_solution name')
class Delete(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, cluster_solution, dataset):
        print('query:Delete')
        print('cluster_solution', cluster_solution)
        print('dataset', dataset)

        '''DELETE'''
        resp = table.delete_one(cluster_solution, [dataset])
        return Response(str(resp), mimetype=mimetype)


# Get rows by dataset.
@ns.route('/get_by/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in TSV format')
    def get(self, dataset):
        '''GET BY DATASET'''
        resp = table.get_by_parent([dataset])
        return Response(str(resp), mimetype=mimetype)


# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "cluster/api/common/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

