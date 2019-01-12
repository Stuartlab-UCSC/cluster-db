
from flask_restplus import Resource


# Update
@ns.route('/update/name/<string:name>/field/<string:field>/value/<string:value>')
@ns.param('value', 'New value')
@ns.param('field', 'Field name')
@ns.param('name', 'Name of ' + table_name + ' to update')
class Update(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, name, field, value):
        '''UPDATE'''
        return table.update(name, field, value)
