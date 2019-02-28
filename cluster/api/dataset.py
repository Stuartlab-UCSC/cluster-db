
# api/dataset.py

from flask import current_app, Response
from flask_restplus import fields, Resource
from cluster.api.restplus import api, mimetype
from cluster.database_update.dataset_table import dataset as table

table_name = 'dataset'
ns = api.namespace('dataset')
model = api.model('dataset', {
    'name': fields.String(required=True, description='Unique dataset name'),
    'uuid': fields.String(description='Universally unique ID'),
    'species': fields.String(description='Species studied'),
    'organ': fields.String(description='source organ'),
    'cell_count': fields.Integer(description='Count of cells in the dataset'),
    'disease': fields.String(description='Any disease of the dataset, i.e. cancer'),
    'platform': fields.String(description='Genomic sequencing platform'),
    'data_source_url': fields.String(description='URL of data source'),
    'publication_url': fields.String(description='URL of publication'),
})

# Get all
@ns.route('/')
class List(Resource):
    @ns.response(200, 'list of all ' + table_name + 's in TSV format')
    def get(self):
        '''GET ALL'''
        return Response(table.get_all(), mimetype=mimetype)
