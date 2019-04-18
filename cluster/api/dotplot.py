from flask_restplus import fields, Resource
from cluster.api.restplus import api
from cluster.api.dbquery import all_for_marker, all_for_marker_dotplot, cluster_similarity
ns = api.namespace('dotplot')

# marker table fields we are exposing as requestable values.
marker_fields = ["sensitivity", "specificity", "accuracy", "precision", "recall", "t_stat", "z_stat",
                 "log2_fold_change_vs_next", "log2_fold_change_vs_min", "mean_expression"]
dotplot_color_fields = marker_fields[5:]
dotplot_size_fields = marker_fields[:5]


marker_values = fields.String(
    required=True,
    description="Values stored for a marker gene.",
    enum=marker_fields
)

dotplot_color_values = fields.String(
    required=True,
    description="Values available for circle color in dotplot.",
    enum=dotplot_color_fields
)

dotplot_size_values = fields.String(
    required=True,
    description="Values available for circle size in dotplot.",
    enum=dotplot_size_fields
)

cluster_name = fields.String(required=True, description='Name of the cluster a circle represents.')

cluster_dotplot_model = api.model("marker-dotplot-values", {
    'name': cluster_name,
    "size": fields.Float(description='Value represented as the size of the circle in a marker vis.'),
    "color": fields.Float(description='Value represented as the color of the circle in a marker vis.'),
    "cell_count": fields.Integer(description="Number of cells in the cluster.")
})

cluster_solutions_dotplot_model = api.model('marker-dotplot-clusters', {
    'dataset_name': fields.String(required=True, description='Name of the dataset the cluster solution was computed on.'),
    'cluster_solution_name': fields.String(required=True, description='Name of the cluster solution'),
    'clusters': fields.List(fields.Nested(cluster_dotplot_model))
})

all_dotplot_model = api.model('marker-dotplot-cluster-solutions',{
    'gene': fields.String(required=True, description='Name of the dataset the cluster solution was computed on.'),
    "size_by": dotplot_size_values,
    "color_by": dotplot_color_values,
    "cluster_solutions": fields.List(fields.Nested(cluster_solutions_dotplot_model))

})

###############################
# Defined for the /marker/<name>/<variable>
cluster_var_model = api.model('marker-values', {
    'name': cluster_name,
    'value': fields.Float(description='Value of a marker in a given cluster.'),
    }
)

marker_model = api.model('marker-clusters', {
    'dataset_name': fields.String(required=True, description='Name of the dataset the cluster solution was computed on.'),
    'cluster_solution_name': fields.String(required=True, description='Name of the cluster solution'),
    'clusters': fields.List(fields.Nested(cluster_var_model))
})

all_markers_model = api.model('marker-cluster-solutions',{
    'gene': fields.String(required=True, description='Name of the dataset the cluster solution was computed on.'),
    "variable": fields.String(required=True, description='Name of variable requested for the markers.'),
    "cluster_solutions": fields.List(fields.Nested(marker_model))

})
#####################################
#cluster_similarity models

cs_size_value = fields.String(
    required=True,
    description="The size of the clusters is the similarity score.",
    enum=["similarity"]
)

cs_color_value = fields.String(
    required=True,
    description="Gene name whose aggregated expression will color the clusters"
)

study_fields = fields.String(
    required=True,
    description="In vivo or in vitro study distinction.",
    enum=["in vivo", "in vitro"]
)

dataset_model = api.model('dataset-model',{
    'name': fields.String(required=True, description='Name of the dataset.'),
    'species': fields.String(required=True, description='The species the data was collected from.'),
    'study': study_fields,
    'organ': fields.String(required=True, description='The organ the data represents.'),
})

similarity_model = api.model('similarity-model', {
    'dataset': fields.Nested(dataset_model),
    'compared_to_cluster': fields.String(required=True, description='The known cell type being compared to unkown clusters.'),
    'cluster_solution_name': fields.String(required=True, description='The cluster solution being compared to the known cell type.'),
    "clusters": fields.List(fields.Nested(cluster_dotplot_model)),
})

all_similarity_model = api.model('all-similarity-model', {
    "dataset_name": fields.String(required=True, description='The data set the known cell types were established in.'),
    "size_by": cs_size_value,
    "color_by": cs_color_value,
    "cluster_solution_name": fields.String(required=True, description='The name for the known cell types.'),
    "cluster_similarities": fields.List(fields.Nested(similarity_model)),
})
#####################################

@ns.route('/marker/<string:name>/<string:variable>')
@ns.param('name', 'Marker gene name, hugo or ensembl')
@ns.param('variable', 'The variable type one of (X, X, X, X)')
class SingleVar(Resource):
    @api.marshal_with(all_markers_model, envelope="resource")
    @ns.response(200, 'marker gene')
    def get(self, name, variable):
        """A list of clustering solutions for a given marker and marker value."""
        return all_for_marker(name, variable)


@ns.route('/marker/<string:name>/dotplot/<string:size>/<string:color>')
@ns.param('name', 'Marker gene name, hugo or ensembl')
@ns.param('size', 'The variable to use as the size of circles')
@ns.param('color', 'The variable to use for the color of circles')
class Marker(Resource):
    @api.marshal_with(all_dotplot_model, envelope="resource")
    @ns.response(200, 'dotplot values for marker gene')
    def get(self, name, size, color):
        """A list of dot plot ready clustering solutions for a given marker with a size and color variable."""

        return all_for_marker_dotplot(name, size, color)


@ns.route('/cluster_solution/<string:cluster_solution_name>/color/<string:gene_name>')
@ns.param('gene_name', 'Marker gene name, matches feature space in centroids')
@ns.param('cluster_solution_name', 'The name for the known cell types.')
class ClusterSolution(Resource):
    @api.marshal_with(all_similarity_model, envelope="resource")
    @ns.response(200, 'cluster solution similarity')
    def get(self, cluster_solution_name, gene_name):
        """A list of clustering solutions for a given marker and marker value."""
        return cluster_similarity(cluster_solution_name, gene_name)
