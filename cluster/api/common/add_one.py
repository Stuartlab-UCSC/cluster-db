
from flask_restplus import Resource
from cluster.api.restplus import api, mimetype


# Add one for tables with no parents.
@ns.route('/add')
class Add_one(Resource):
    @ns.expect(model)
    @ns.response(200, 'database row ID')
    def post(self):
        '''ADD ONE'''
        resp = table.add_one(api.payload)
        return Response(str(resp), mimetype=mimetype)
