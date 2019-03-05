from flask_restplus import fields, Resource
from cluster.api.restplus import api
from cluster.database.tableaccess import engine, dataset, alldatasets, cluster_solution, cluster_solutions_per_dataset
table_name = 'datasets'
ns = api.namespace('dataset')
model = api.model('dataset', {
    'name': fields.String(required=True, description='Unique dataset name'),
    'description': fields.String(description='Unique dataset name'),
    'id': fields.String(description='Access identifier for the data set')
})

cs_model = api.model('cluster_solution', {
    'name': fields.String(required=True, description='Curator made identifier'),
    'method': fields.String(description='Curator method identifier'),
    "id": fields.String(description='Access identifier for the cluster solution')}
                     )

@ns.route('/')
class DatasetList(Resource):
    @api.marshal_with(model, envelope="resource")
    @ns.response(200, 'list of all datasets, with name, description, and id')
    def get(self):
        """a list of data sets: name, description, and id."""
        return alldatasets(dataset, engine.connect())

@ns.route('/<int:id>/cluster-solutions')
@ns.param('id', 'Data set identifier')
class ClusterSolsForDataset(Resource):
    @api.marshal_with(cs_model, envelope="resource")
    @ns.response(200, 'list of available clustering solutions for a dataset')
    def get(self, id):
        """a list of available cluster solutions for a data set: name, method and id."""

        return cluster_solutions_per_dataset(
            cluster_solution,
            dataset,
            id,
            engine.connect()
        )
