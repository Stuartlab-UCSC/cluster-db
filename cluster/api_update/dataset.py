
# api/dataset.py

from flask import current_app, Response
from flask_restplus import fields, Resource
from cluster.api.restplus import api, mimetype
from cluster.database_update.dataset_table import dataset as table

table_name = 'dataset'
ns = api.namespace('dataset-update')
model = api.model('dataset', {
    'name': fields.String(required=True, description='Unique dataset name'),
    'uuid': fields.String(description='Universally unique ID'),
    'species': fields.String(description='Species studied'),
    'organ': fields.String(description='source organ'),
    'cell_count': fields.Integer(description='Count of cells in the dataset'),
    'disease': fields.String(description='Any disease of the dataset, i.e. cancer'),
    'platform': fields.String(description='Genomic sequencing platform'),
    'description': fields.String(description='Short description'),
    'data_source_url': fields.String(description='URL of data source'),
    'publication_url': fields.String(description='URL of publication'),
})


# Add from TSV file.
@ns.route('/add/tsv_file/<string:tsv_file>')
@ns.param('tsv_file', 'TSV file name')
class Add_tsv(Resource):
    @ns.response(200, 'last database row ID added')
    def get(self, tsv_file):
        '''ADD MANY FROM TSV FILE'''
        resp = table.add_tsv(tsv_file)
        return Response(str(resp), mimetype=mimetype)


# Do the equivalent of a bash shell 'source' to include the routes.
filename = "cluster/api_update/common/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/delete_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/get_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
