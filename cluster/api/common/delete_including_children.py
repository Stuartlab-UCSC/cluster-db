
from flask_restplus import Resource


# Delete including children
@ns.route('/delete_including_children/name/<string:name>')
@ns.param('name', 'Name of ' + table_name + ' to delete')
class Delete_with_children(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, name):
        '''DELETE, INCLUDING ALL CHILDREN'''
        return table.delete_including_children(name)
