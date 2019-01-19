
from flask import Response
from flask_restplus import Resource
from cluster.api.restplus import api, mimetype


# Add one for tables with a dataset grandparent.
@ns.route('/add_by/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
class Add_one(Resource):
    @ns.expect(model)
    @ns.response(200, 'database row ID')
    def post(self, dataset):
        '''ADD ONE'''
        resp = table.add_one(api.payload, [dataset])
        return Response(str(resp), mimetype=mimetype)

