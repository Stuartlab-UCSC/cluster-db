
# This file contains the basic routes for each table.
# It should be included in the table route file with exec().

from flask_restplus import Resource
from cluster.api.restplus import api, model_id


# Get all
@ns.route('/')
class List(Resource):
    @ns.response(200, 'list of all as JSON or TSV')
    def get(self):
        '''GET ALL'''
        return table.get()

# Add one
    @ns.expect(model)
    @ns.response(200, 'Success with ID of added')
    def post(self):
        '''ADD ONE'''
        return table.add(api.payload)


# Get one
@ns.route('/<string:name>')
@ns.param('name', 'The name')
class GetOne(Resource):
    @ns.response(404, 'Not found')
    @ns.marshal_with(model)
    def get(self, name):
        '''GET ONE'''
        return table.get(name)


# Update
@ns.route('/update/name/<string:name>/field/<string:field>/value/<string:value>')
@ns.param('value', 'New value')
@ns.param('field', 'Field name')
@ns.param('name', 'Row name')
class Update(Resource):
    @ns.response(200, 'Success with ID of updated')
    @ns.response(404, 'Not found')
    @ns.marshal_with(model_id)
    def put(self, name, field, value):
        '''UPDATE'''
        return table.update(name, field, value)


# Delete
@ns.route('/delete/name/<string:name>')
@ns.param('name', 'Row name')
class Delete(Resource):
    @ns.response(200, 'Success with ID of deleted')
    @ns.response(404, 'Not found')
    @ns.marshal_with(model_id)
    def delete(self, name):
        '''DELETE'''
        return table.delete(name)


#if __name__ == '__main__':
#    app.run(debug=True)
