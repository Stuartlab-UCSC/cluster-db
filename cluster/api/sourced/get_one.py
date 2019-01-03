
# This file contains the basic routes for each table.
# It should be included in the table route file with exec().

from flask_restplus import Resource


# Get one
@ns.route('/<string:name>')
@ns.param('name', 'name of the ' + table_name + ' to get')
class Get_one(Resource):
    @ns.response(200, table_name + ' in JSON or TSV format')
    @ns.response(404, 'Not found')
    @ns.marshal_with(model)
    def get(self, name):
        '''GET ONE'''
        return table.get_one(name, request.accept_mimetypes)
