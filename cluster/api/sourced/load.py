
# This file contains the routes to load TSV files for any table.
# It should be included in the table route file with exec().

from flask_restplus import Resource


# Load TSV
@ns.route('/load/parent_name/<string:parent_name>/tsv_file/<string:tsv_file>')
@ns.param('tsv_file', 'TSV file path')
@ns.param('parent_name', 'Name of parent this ' + table_name + ' belongs to')
class Load_tsv(Resource):
    @ns.response(200, 'Success with row count of added')
    def get(self, parent_name, tsv_file):
        '''LOAD TSV FILE'''

        print('!!!!!! get():parent_name:', parent_name)

        return table.load_tsv(parent_name, tsv_file)
