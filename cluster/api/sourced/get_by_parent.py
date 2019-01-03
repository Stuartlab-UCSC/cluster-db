
# This file contains the routes to get rows for any table.
# It should be included in the table route file with exec().

from flask_restplus import Resource


# Get rows by parent (foreign key) name.
@ns.route('/get_by_parent/<string:parent_name>')
@ns.param('parent_name', 'parent name of the ' + table_name + ' to get')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in JSON or TSV format')
    def get(self, parent_name):
        '''GET BY PARENT'''
        return table.get_by_parent(parent_name, request.accept_mimetypes)
