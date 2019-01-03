
# This file contains the routes to load TSV files for any table.
# It should be included in the table route file with exec().

from flask_restplus import Resource


# Load TSV
# TODO there is a better way to route with optional parameters
@ns.route('/load/tsv_file/<string:tsv_file>')
@ns.route('/load/tsv_file/<string:tsv_file>/parent_names/<string:parent_names>')
@ns.param('tsv_file', 'TSV file path')
@ns.param('parent_names', 'comma-separated names of parents')
class Load_tsv(Resource):
    @ns.response(200, 'Success with row count of added')
    def get(self, tsv_file, parent_names=None):
        '''LOAD TSV FILE'''
        return table.load_tsv(tsv_file, parent_name)
