
from flask_restplus import Resource


# Add many from TSV file.
# TODO there is a better way to route with optional parameters
@ns.route('/add_many/tsv_file/<string:tsv_file>')
@ns.route('/add_many/tsv_file/<string:tsv_file>/parent_names/<string:parent_names>')
@ns.param('tsv_file', 'TSV file path')
@ns.param('parent_names', 'comma-separated names of parents')
class Add_many_tsv_file(Resource):
    @ns.response(200, 'Success with row count of added')
    def get(self, tsv_file, parent_names=None):
        '''ADD MANY FROM TSV FILE'''
        return table.add_many_tsv_file(tsv_file, parent_name)
