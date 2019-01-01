
# This file contains the "get all" route per table.
# It should be included in the table route file with exec().

from flask_restplus import Resource


# Get all
@ns.route('/')
class List(Resource):
    @ns.response(200, 'list of all ' + table_name + 's in JSON or TSV format')
    def get(self):
        '''GET ALL'''
        return table.get_all()
