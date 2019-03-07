
# api/query.py
# Generic read query in SGL

from flask import Response
from flask_restplus import Resource
from cluster.api.restplus import api, mimetype
from cluster.database.query import query as database_query

ns = api.namespace('sql')


@ns.route('/<string:sql>')
@ns.param('sql', 'SQL read-only query string')
class List(Resource):
    @ns.response(200, 'Result of query')
    def get(self, sql):
        '''Generic read-only queries using raw sql.'''
        resp = database_query(sql)
        return Response(str(resp), mimetype=mimetype)