from flask_restplus import fields, Resource
from cluster.api.restplus import api
from cluster.api.dbquery import all_for_marker, all_for_marker_dotplot
ns = api.namespace('marker')

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

dataset_model = api.model("dataset_model", {
    "name": fields.String(required=True, description='Name of the dataset the cluster solution was computed on.'),
    "species": fields.String(required=True, description='None'),
    "study": fields.String(required=True, description='None'),
    "organ": fields.String(required=True, description='None'),
})
cluster_solutions_dotplot_model = api.model('marker-dotplot-clusters', {
    'dataset': fields.Nested(dataset_model),
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

@ns.route('/<string:name>/<string:variable>')
@ns.param('name', 'Marker gene name, hugo or ensembl')
@ns.param('variable', 'The variable type one of (X, X, X, X)')
class SingleMarkerVar(Resource):
    @api.marshal_with(all_markers_model, envelope="resource")
    @ns.response(200, 'marker gene')
    def get(self, name, variable):
        """A list of clustering solutions for a given marker and marker value."""
        return all_for_marker(name, variable)


@ns.route('/<string:name>/dotplot/<string:size>/<string:color>')
@ns.param('name', 'Marker gene name, hugo or ensembl')
@ns.param('size', 'The variable to use as the size of circles')
@ns.param('color', 'The variable to use for the color of circles')
class Marker(Resource):
    @api.marshal_with(all_dotplot_model, envelope="resource")
    @ns.response(200, 'dotplot values for marker gene')
    def get(self, name, size, color):
        """A list of dot plot ready clustering solutions for a given marker with a size and color variable."""
        return all_for_marker_dotplot(name, size, color)