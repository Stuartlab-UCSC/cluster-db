
# api/clustering_solution.py

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
    'secondary': fields.Integer(required=True,
        description='One means this is a secondary clustering solution and another clustering solution is the default'),
    'dataset': fields.String(required=True, description='Name of dataset that was analyzed'),
})


# Add many from TSV file.
@ns.route('/add_many/tsv_file/<string:tsv_file>/dataset/<string:dataset_name>')
@ns.param('tsv_file', 'TSV file path')
@ns.param('dataset_name', 'name of parent dataset')
class Add_many_tsv_file(Resource):
    @ns.response(200, 'Success')
    def get(self, tsv_file, dataset_name):
        '''ADD MANY FROM TSV FILE'''
        return table.add_many_tsv_file(tsv_file, dataset_name)


# Get rows by parent (foreign key) name.
@ns.route('/get_by_dataset/<string:dataset_name>')
@ns.param('dataset_name', 'name of parent dataset')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in JSON or TSV format')
    def get(self, dataset_name):
        '''GET BY DATASET'''
        return table.get_by_parent(dataset_name, request.accept_mimetypes)


# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/delete.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

