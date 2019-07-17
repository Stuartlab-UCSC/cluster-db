from flask_restplus import fields, Resource
from flask_user import current_user
from cluster.api.restplus import api
from cluster.api.cluster_solution import ca_model
from cluster.api.dbquery import all_datasets, cluster_solutions, cluster_solution_id, cell_assignments

ns = api.namespace('dataset')

model = api.model('dataset', {
    'name': fields.String(required=True, description='Unique dataset name.'),
    'description': fields.String(description='Data set description.'),
    'id': fields.String(description='Identifier for accessing the data set.')
})

cs_model = api.model('cluster_solution', {
    'name': fields.String(required=True, description='Curator made name for the clustering solution.'),
    'method': fields.String(description='Curator made name for the method used.'),
    "id": fields.String(description='Identifier for accessing the cluster solution.')
})


@ns.route('/')
class DataSetList(Resource):
    @api.marshal_with(model, envelope="resource")
    @ns.response(200, 'datasets')
    def get(self):
        """A list of data sets: name, description, and id."""
        return all_datasets()


@ns.route('/<int:id>/cluster-solutions')
@ns.param('id', 'Data set identifier')
class ClusterSolsForDataSet(Resource):
    @api.marshal_with(cs_model, envelope="resource")
    @ns.response(200, 'cluster solutions')
    def get(self, id):
        """A list of available cluster solutions for a data set: name, method and id."""
        return cluster_solutions(id)


@ns.route('/<string:dataset_name>/cluster-solution/<string:cluster_solution_name>/cell-assignments')
@ns.param('dataset_name', 'Data set name')
@ns.param('cluster_solution_name', 'Cluster solution name')
class CellAssignmentsForAClusterSolution(Resource):
    @api.marshal_with(ca_model, envelope="resource")
    @ns.response(200, 'cluster solutions')
    def get(self, dataset_name, cluster_solution_name):
        """The dataset cell assignments for a cluster solution"""

        cs_id = cluster_solution_id(
            dataset_name,
            cluster_solution_name,
        )

        return cell_assignments(cs_id)
