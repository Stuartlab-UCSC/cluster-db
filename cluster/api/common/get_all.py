
from flask import request
from flask_restplus import Resource


# Get all
@ns.route('/')
class List(Resource):
    @ns.response(200, 'list of all ' + table_name + 's in JSON or TSV format')
    def get(self):
        '''GET ALL'''
        return table.get_all(request.accept_mimetypes)
