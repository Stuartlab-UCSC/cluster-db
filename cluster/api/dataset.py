from flask_restplus import fields, Resource
from cluster.api.restplus import api
import cluster.database.models as tables
from cluster.database.access import all_datasets, cluster_solutions, engine


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

        return all_datasets(
            tables.dataset,
            engine.connect()
        )


@ns.route('/<int:id>/cluster-solutions')
@ns.param('id', 'Data set identifier')
class ClusterSolsForDataSet(Resource):
    @api.marshal_with(cs_model, envelope="resource")
    @ns.response(200, 'cluster solutions')
    def get(self, id):
        """A list of available cluster solutions for a data set: name, method and id."""

        return cluster_solutions(
            tables.cluster_solution,
            tables.dataset,
            id,
            engine.connect()
        )
