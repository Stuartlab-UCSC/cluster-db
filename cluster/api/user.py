"""
Protected user enpoints work accessing cell type worksheets.
"""
from flask import send_file, request, abort
from flask_restplus import Resource
from flask_user import current_user
from cluster.api.restplus import api
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import io
from cluster.database.user_models import get_all_worksheet_paths
from cluster.database.filename_constants import MARKER_TABLE
from cluster.database.user_models import (
    WorksheetUser,
    User,
    UserExpression,
    ExpCluster,
    ClusterGeneTable
)
from cluster.user_io import (
    read_markers_df,
    read_saved_worksheet,
    read_gene_expression,
    read_cluster,
    read_xys,
    save_worksheet
)
matplotlib.use("Agg")
ns = api.namespace('user')


@ns.route('/worksheets')
class UserWorksheets(Resource):
    @ns.response(200, 'worksheet retrieved', )
    def get(self):
        """Retrieve a list of available worksheets available to the user """
        print(current_user.email)
        if not current_user.is_authenticated:
            return abort(403)

        return WorksheetUser.get_user_worksheet_names(current_user)


@ns.route('/<string:user>/worksheet/<string:worksheet>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
class Worksheet(Resource):
    @ns.response(200, 'worksheet retrieved', )
    def get(self, user, worksheet):
        """Retrieve a saved worksheet."""
        if not current_user.is_authenticated:
            return abort(403)
        print(user)
        print("#### current user", current_user.email)
        owns_data = current_user.email == user

        if owns_data:
            worksheet = WorksheetUser.get_worksheet(current_user, worksheet)
            return read_saved_worksheet(worksheet.place)

        return abort(401, "User emails did not match, currently users may only access their own data.")

    @ns.response(200, 'worksheet received')
    def post(self, user, worksheet):
        """Save a worksheet"""
        if not current_user.is_authenticated:
            return abort(403)

        if request.get_json() is None:
            raise ValueError("json state representation required in body of request")

        owns_data = current_user.email == user

        if owns_data:

            user_entry = User.get_by_email(user)
            ws_entry = WorksheetUser.get_worksheet(user_entry, worksheet)
            save_worksheet(ws_entry.place, request.get_json())


@ns.route('/<string:user>/worksheet/<string:worksheet>/cluster/<string:cluster_name>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
@ns.param('cluster_name', 'The name of the cluster')
class GeneTable(Resource):
    # @api.marshal_with(all_markers_model, envelope="resource")
    @ns.response(200, 'tab delimited genes per cluster file', )
    def get(self, user, worksheet, cluster_name):
        """Grab gene metrics for a specified cluster."""
        if not current_user.is_authenticated:
            return abort(403)

        user_entry = User.get_by_email(user)
        ws_entry = WorksheetUser.get_worksheet(user_entry, worksheet_name=worksheet)
        exp_entry = UserExpression.get_by_worksheet(ws_entry)
        cluster_entry = ExpCluster.get_cluster(exp_entry)
        path = ClusterGeneTable.get_table(cluster_entry).place

        # Make the table and then throw it in a byte buffer to pass over.
        gene_table = read_markers_df(path)
        msk = (gene_table["cluster"] == cluster_name).tolist()

        gene_table = gene_table.iloc[msk]
        cluster_not_there = gene_table.shape[0] == 0
        if cluster_not_there:
            abort(422, "The cluster requested has no values in the gene table")

        gene_table = gene_table.drop("cluster", axis=1)

        buffer = io.StringIO()

        gene_table.to_csv(buffer, index=False, sep="\t")
        buffer.seek(0)

        resp = {
            "cluster_name": cluster_name,
            "gene_table": buffer.getvalue()
        }

        return resp


@ns.route('/<string:user>/worksheet/<string:worksheet>/gene/<string:gene_name>/color/<string:color_by>/size/<string:size_by>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
@ns.param('color_by', 'A metric on the gene that can be used as a color variable')
@ns.param('size_by', 'A metric on the gene that can be used as a size variable')
@ns.param('gene_name', 'A valid gene name')
class AddGene(Resource):
    # @api.marshal_with(all_markers_model, envelope="resource")
    @ns.response(200, 'Color by and size by as rows and columns as clusters', )
    def get(self, user, worksheet, color_by, size_by, gene_name):
        """Grab color and size gene metrics for a specified gene."""
        if not current_user.is_authenticated:
            return abort(403)
        # Make the table and then throw it in a byte buffer to pass over.
        user_entry = User.get_by_email(user)
        ws_entry = WorksheetUser.get_worksheet(user_entry, worksheet_name=worksheet)
        exp_entry = UserExpression.get_by_worksheet(ws_entry)
        cluster_entry = ExpCluster.get_cluster(exp_entry)
        path = ClusterGeneTable.get_table(cluster_entry).place
        # Make the table and then throw it in a byte buffer to pass over.
        gene_table = read_markers_df(path)

        buffer = io.StringIO()
        gt = dotplot_values(gene_table, gene=gene_name, color_by=color_by, size_by=size_by)
        gt.to_csv(buffer, sep="\t")
        buffer.seek(0)

        mem = io.BytesIO()
        mem.write(buffer.getvalue().encode("utf-8"))
        mem.seek(0)

        return send_file(
            mem,
            mimetype="text/tsv"
        )


@ns.route('/<string:user>/worksheet/<string:worksheet>/var_name/<string:var_name>/genes/<string:genes>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
@ns.param('var_name', 'A valid variable name in the gene table')
@ns.param('genes', 'Comma separated gene names available in the gene table')
class DotplotValues(Resource):
    # @api.marshal_with(all_markers_model, envelope="resource")
    @ns.response(200, 'tab delimited genes per cluster file', )
    def get(self, user, worksheet, var_name, genes):
        """Grab gene metrics for a specified cluster."""
        if not current_user.is_authenticated:
            return abort(403)

        doesnt_own_data = current_user.email != user
        if doesnt_own_data:
            return abort(401, "User emails did not match, currently users may only access their own data.")

        path_dict = get_all_worksheet_paths(user, worksheet)
        genes = genes.strip().split(",")
        # Make the table and then throw it in a byte buffer to pass over.
        markers_df = read_markers_df(path_dict[MARKER_TABLE])
        table = bubble_table(markers_df, genes, var_name)

        buffer = io.StringIO()
        table.to_csv(buffer, sep="\t")
        buffer.seek(0)

        mem = io.BytesIO()
        mem.write(buffer.getvalue().encode("utf-8"))
        mem.seek(0)

        return send_file(
            mem,
            mimetype="text/tsv"
        )


@ns.route('/<string:user>/worksheet/<string:worksheet>/scatterplot/<string:type>/gene/<string:gene>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
@ns.param('type', 'tsne, umap, or pca.')
@ns.param('gene', 'A gene name present in the expression matrix')
class GeneScatterplot(Resource):
    @ns.response(200, 'png scatterplot image')
    def get(self, user, worksheet, type, gene):
        """A png of a scatter plot colored by a genes value"""
        if not current_user.is_authenticated:
            return abort(403)

        from cluster.database.user_models import ExpDimReduct
        # Make the table and then throw it in a byte buffer to pass over.
        user_entry = User.get_by_email(user)
        ws_entry = WorksheetUser.get_worksheet(user_entry, worksheet_name=worksheet)
        exp_entry = UserExpression.get_by_worksheet(ws_entry)
        cluster_entry = ExpCluster.get_cluster(exp_entry)
        xy_entry = ExpDimReduct.get_by_expression(exp_entry)

        cluster = read_cluster(cluster_entry.place)

        xys = read_xys(xy_entry.place)

        centers = centroids(xys, cluster)

        gene = read_gene_expression(exp_entry.place, gene)
        png = scatter_continuous(xys, centers, gene)

        return send_file(
            png,
            mimetype='image/png'
        )


@ns.route('/<string:user>/worksheet/<string:worksheet>/scatterplot/<string:type>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
@ns.param('type', 'tsne, umap, or pca.')
class ClusterScatterplot(Resource):
    @ns.response(200, 'png scatterplot image')
    def post(self, user, worksheet, type):
        """A png scatterplot with clusters colored by json color map."""
        if not current_user.is_authenticated:
            return abort(403)

        from cluster.database.user_models import ExpDimReduct
        # Make the table and then throw it in a byte buffer to pass over.
        user_entry = User.get_by_email(user)
        ws_entry = WorksheetUser.get_worksheet(user_entry, worksheet_name=worksheet)
        exp_entry = UserExpression.get_by_worksheet(ws_entry)
        cluster_entry = ExpCluster.get_cluster(exp_entry)
        xy_entry = ExpDimReduct.get_by_expression(exp_entry)

        cluster = read_cluster(cluster_entry.place)

        xys = read_xys(xy_entry.place)

        centers = centroids(xys, cluster)

        if not request.is_json:
            return abort(422, "The post requires json to specify a color map")

        try:
            colors = request.get_json()
            color_map = dict(
                zip(
                    colors["cluster-name"],
                    colors["colors"]
                )
            )

        except KeyError:
            abort(422, "Malformed json, requires a 'cluster-name' and 'colors' array")

        return send_file(
            scatter_categorical(xys, centers, color_map, cluster),
            mimetype='image/png'
        )


def scatter_categorical(xys, centers, color_map, clusters):
    """
    Return an io.BytesIO object that is a jpeg image. Can be sent with send_file.
    :param xys:
    :param centers:
    :param color_map:
    :param clusters:
    :return:
    """
    plt.axis('off')
    data = pd.concat([xys, clusters], axis=1)
    data.head()
    data.columns = ["x", "y", "cluster"]
    for label in centers.index:
        plt.scatter(
            x=data.loc[data['cluster'] == label, 'x'],
            y=data.loc[data['cluster'] == label, 'y'],
            color=color_map[label],
            alpha=0.7,
        )

        plt.annotate(
            label,
            (centers.loc[label]["x"], centers.loc[label]["y"]),
            horizontalalignment='center',
            verticalalignment='center',
            size=15, weight='bold',
            color="black"
        )

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes)
    img_bytes.seek(0)
    plt.close()
    return img_bytes


def scatter_continuous(xys, centers, gene):
    """
    Return an io.BytesIO object that is a jpeg image. Can be sent with send_file.
    :param xys:
    :param centers:
    :param gene:
    :return:
    """
    plt.axis('off')
    cm = plt.cm.get_cmap('coolwarm')
    sc = plt.scatter(x=xys['x'], y=xys['y'], c=gene, alpha=0.7, cmap=cm, norm=None, edgecolor='none')

    # Annotate the clusters at their centroids.
    for label in centers.index:
        plt.annotate(
            label,
            (centers.loc[label]["x"], centers.loc[label]["y"]),
            horizontalalignment='center',
            verticalalignment='center',
            size=15, weight='bold',
            color="black"
        )

    plt.colorbar(sc)
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png")
    img_bytes.seek(0)
    plt.close()
    return img_bytes


def centroids(xys, cluster):
    """Returns a dataframe with cluster as index and x and y centroid columns."""
    both = pd.concat([xys, cluster], axis=1)
    both.columns = ["x", "y", "cluster"]
    cluster_centers = both.groupby("cluster").mean()
    # Clusters are represented as strings.
    cluster_centers.index = [str(c) for c in cluster_centers.index]
    return cluster_centers


def dotplot_values(gene_table, gene, color_by="mean_expression", size_by="sensitivity"):
    gene_table = gene_table.iloc[(gene_table["gene"] == gene).tolist()]

    gene_not_found = not gene_table.shape[0]

    if gene_not_found:
        return abort(404, "'%s' gene was not found in the markers table" % gene)

    bubble_values = gene_table[["cluster", size_by, color_by]].transpose()
    bubble_values.columns = bubble_values.loc["cluster"]
    bubble_values.drop("cluster", axis=0, inplace=True)

    return bubble_values


def gene_table(marker_df, cluster_name):
    """Creates a gene table on the fly for a particulat cluster and clustersolution from marker dictionaries."""

    msk = (marker_df["cluster"] == cluster_name).tolist()
    marker_df = marker_df.iloc[msk]

    return marker_df


def dataframe_to_str(df, index=True):
    buffer = io.StringIO()
    df.to_csv(buffer, sep="\t", header=True, index=index)
    buffer.seek(0)
    return buffer.getvalue()


def bubble_table(marker_df, genes, attr_name):
    """Creates a size or color table for the worksheet endpoint."""
    if genes is None or marker_df is None:
        return None

    msk = marker_df["gene"].isin(genes).tolist()
    bubble_values = marker_df.iloc[msk][["gene", "cluster", attr_name]]
    bubble_values = bubble_values.pivot(
        index="gene",
        columns="cluster",
        values=attr_name
    )

    return bubble_values
