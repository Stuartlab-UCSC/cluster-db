
# api/cluster_solution.py

from flask_restplus import fields, Resource
from cluster.api.restplus import api
from cluster.database.tableaccess import cellassignments, engine, cluster_assignment, cluster, cluster_solution
table_name = 'cluster_solution'
ns = api.namespace('cluster-solution')
ca_model = api.model('cluster-assignment', {
    'name': fields.String(required=True, description='identifier for the cell (within a data set)'),
    'cluster_name': fields.String(description='string identifier for the cluster')
    }
)
@ns.route('/<int:id>/cell-assignments')
@ns.param('id', 'Cluster solution identifier')
class CellAssignment(Resource):
    @api.marshal_with(ca_model, envelope="resource")
    @ns.response(200, '')
    def get(self, id):
        """cluster assignments of cells in a clustering solution."""

        return cellassignments(
            cluster_assignment,
            cluster,
            cluster_solution,
            id,
            engine.connect()
        )
