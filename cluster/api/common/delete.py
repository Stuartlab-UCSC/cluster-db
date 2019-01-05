
# This file contains the basic routes for each table.
# It should be included in the table route file with exec().

from flask_restplus import Resource


# Delete
@ns.route('/delete/name/<string:name>')
@ns.param('name', 'Name of ' + table_name + ' to delete')
class Delete(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, name):
        '''DELETE'''
        return table.delete(name)
