
from flask import request, Response
from flask_restplus import Resource
from cluster.api.restplus import mimetype


# Get all
@ns.route('/')
class List(Resource):
    @ns.response(200, 'list of all ' + table_name + 's in TSV format')
    def get(self):
        '''GET ALL'''
        return Response(table.get_all(), mimetype=mimetype)
