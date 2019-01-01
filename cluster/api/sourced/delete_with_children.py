
# This file contains the basic routes for each table.
# It should be included in the table route file with exec().

from flask_restplus import Resource


# Delete with children
@ns.route('/delete_with_children/name/<string:name>')
@ns.param('name', 'Name of ' + table_name + ' to delete')
class Delete_with_children(Resource):
    @ns.response(200, 'Success with ID of deleted')
    @ns.response(404, 'Not found')
    def get(self, name):
        '''DELETE, INCLUDING ALL CHILDREN'''
        return table.delete_with_children(name)
