
from flask_restplus import Resource
from cluster.api.restplus import mimetype


# Delete for tables with no parents.
@ns.route('/delete/<string:name>')
@ns.param('name', 'Name of ' + table_name + ' to delete')
class Delete(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, name):
        '''DELETE'''
        resp = table.delete_one(name)
        return Response(str(resp), mimetype=mimetype)
