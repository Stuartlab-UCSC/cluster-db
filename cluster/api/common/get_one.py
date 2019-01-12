
from flask import request
from flask_restplus import Resource


# Get one
@ns.route('/<string:name>')
@ns.param('name', table_name + ' name')
class Get_one(Resource):
    @ns.response(200, table_name + ' in JSON or TSV format')
    @ns.response(404, 'Not found')
    def get(self, name):
        '''GET ONE'''
        return table.get_one(name, request.accept_mimetypes)
