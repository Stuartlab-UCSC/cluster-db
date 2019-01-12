
from flask_restplus import Resource
from cluster.api.restplus import api


# Add one for tables with no parent.
@ns.route('/add')
class Add_one(Resource):
    @ns.expect(model)
    @ns.response(200, 'Success')
    def post(self):
        '''ADD ONE'''
        return table.add_one(api.payload)
