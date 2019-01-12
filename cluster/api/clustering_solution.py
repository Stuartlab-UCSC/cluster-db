
# api/clustering_solution.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.clustering_solution_table import clustering_solution as table

table_name = 'clustering solution'
ns = api.namespace('clustering_solution')
model = api.model('clustering_solution', {
    'name': fields.String(required=True, description='Unique clustering solution name'),
    'method': fields.String(required=True, description='Clustering method applied'),
    'method_implementation': fields.String(required=True, description='Clustering method implementation'),
    'method_url': fields.String(required=True, description='URL of clustering solution method'),
    'method_parameters': fields.String(required=True, description='Clustering method parameters'),
    'analyst': fields.String(required=True, description='Person who ran the analysis'),
    'secondary': fields.Integer(required=True, \
        description='One means this is a secondary clustering solution and some other clustering solution is the default'),
    'dataset': fields.String(required=True, description='Name of dataset that was analyzed'),
})

# Add from TSV file.
@ns.route('/add' + \
    '/tsv_file/<string:tsv_file>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'name of dataset')
@ns.param('tsv_file', 'TSV file name')
class Add_tsv(Resource):
    @ns.response(200, 'Success')
    def get(self, tsv_file, dataset):
        '''ADD FROM TSV FILE BY CLUSTERING_SOLUTION'''
        return table.add_tsv(tsv_file, ['dataset1'])

"""
# Delete.
@ns.route('/delete_by/dataset/<string:dataset>')
@ns.param('dataset', 'name of dataset')
class Delete_by_dataset(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, dataset):
        '''DELETE'''
        return table.delete(dataset)
"""

# Get rows by dataset.
@ns.route('/get_by/dataset/<string:dataset>')
@ns.param('dataset', 'name of parent dataset')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in JSON or TSV format')
    def get(self, dataset):
        '''GET BY DATASET'''
        return table.get_by_parent([dataset], request.accept_mimetypes)


# Just debugging:
#filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_all.py"
#exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

# Do the equivalent of a bash shell 'source' to get the base routes.
#filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/update.py"
#exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

