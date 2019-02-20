
# api/query.py
# Generic read query in SGL

from flask import request, Response
from flask_restplus import fields,  Resource
from cluster.api.restplus import api, mimetype
from cluster.database.query import query as database_query

ns = api.namespace('sql')


@ns.route('/<string:sql>')
@ns.param('sql', 'SQL query string')
class List(Resource):
    @ns.response(200, 'Result of query')
    def get(self, sql):
        '''SQL QUERY'''
        resp = database_query(sql)
        return Response(str(resp), mimetype=mimetype)


"""
cellDbRoutes = Blueprint('cellDbRoutes', __name__)
appCtx = getAppCtx()

# Handle the route to get all of the cell dataset data from the DB.
@cellDbRoutes.route('/cell/dataset/getAll', methods=['GET'])
def getAll():
    data = cellDataset.getAll(appCtx)
    raise SuccessResp(data)
"""