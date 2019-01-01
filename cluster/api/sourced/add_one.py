
# This file contains the basic routes for each table.
# It should be included in the table route file with exec().

from flask_restplus import Resource
from cluster.api.restplus import api


# Add one
@ns.route('/add')
class Add(Resource):
    @ns.expect(model)
    @ns.response(200, 'Success with ID of added')
    def post(self):
        '''ADD ONE'''
        return table.add_one(api.payload)
