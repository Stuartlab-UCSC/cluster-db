
from flask import request, Response
from flask_restplus import Resource
from cluster.api.restplus import mimetype


# Get one
@ns.route('/<string:name>')
@ns.param('name', table_name + ' name')
class Get_one(Resource):
    @ns.response(200, table_name + ' in TSV format')
    @ns.response(404, 'Not found')
    def get(self, name):
        '''GET ONE'''
        resp = table.get_one(name)
        return Response(str(resp), mimetype=mimetype)
