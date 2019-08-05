from flask_restplus import fields, Resource
from cluster.api.restplus import api
from cluster.api.dbquery import cell_assignments

ns = api.namespace('cluster-solution')

ca_model = api.model('cell-assignment', {
    'name': fields.String(required=True, description='Identifier for the cell (within a data set).'),
    'cluster_name': fields.String(description='Curator given name for the cluster.')
    }
)


@ns.route('/<int:id>/cell-assignments')
@ns.param('id', 'Cluster solution identifier')
class CellAssignment(Resource):
    @api.marshal_with(ca_model, envelope=None)
    @ns.response(200, 'cell assignments')
    def get(self, id):
        """A list of cell assignments for a clustering solution."""

        return cell_assignments(id)
