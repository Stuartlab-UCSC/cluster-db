"""
A mock up of future user protected endpoints.
"""
from flask import send_file, request
from flask_restplus import Resource
from cluster.api.restplus import api
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import gzip
import json


# These are all the global variables that will need access functions once the data serves more than worksheet.
TEST_STATE_PATH = "./users/tests/test_state.json"
TEST_CLUSTER_TABLE_PATH = "./users/test/clusters_table.tab"
TEST_MARKERS_DICT_PATH = "./users/test/krigstien6000k_markers.json.gzip"
TEST_EXPRESSION_PICKLE_PATH = "./users/test/exp.pi"
TEST_CLUSTER_ID_PATH = "./users/test/louvain:res:1.50.pi"
TEST_XY_PATH = "./users/test/X_umap.pi"

# The cluster solution name matches what is int the cluster-id file and a key inside the markers.json.gzip
CLUSTER_SOLUTION_NAME = "louvain:res:1.50"


ns = api.namespace('user')
@ns.route('/<string:user>/worksheet/<string:worksheet>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
class Worksheet(Resource):
    # @api.marshal_with(all_markers_model, envelope="resource")
    @ns.response(200, 'worksheet retrieved', )
    def get(self, user, worksheet):
        """Retrieve a saved worksheet."""
        resp = grab_saved_worksheet(user, worksheet) or generate_worksheet(user, worksheet)
        return resp

    @ns.response(200, 'worksheet recieved')
    def post(self, user, worksheet):
        """Save a worksheet"""
        save_worksheet(user, worksheet, request.get_json())


@ns.route('/<string:user>/worksheet/<string:worksheet>/cluster/<string:cluster_name>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
@ns.param('cluster_name', 'The name of the cluster')
class GeneTable(Resource):
    # @api.marshal_with(all_markers_model, envelope="resource")
    @ns.response(200, 'tab delimited genes per cluster file', )
    def get(self, user, worksheet, cluster_name):
        """Gene metric value tab separated file for a single metric."""

        # Make the table and then throw it in a byte buffer to pass over.
        markers_file_name=TEST_MARKERS_DICT_PATH
        marker_dicts = read_json_gzipd(markers_file_name)["markers"]

        buffer = io.StringIO()
        gt = gene_table(marker_dicts, cluster_name)
        gt.to_csv(buffer, index=False, sep="\t")
        buffer.seek(0)

        mem = io.BytesIO()
        mem.write(buffer.getvalue().encode('utf-8'))
        mem.seek(0)

        return send_file(
            mem,
            mimetype='text/tsv',
        )


@ns.route('/<string:user>/worksheet/<string:worksheet>/scatterplot/<string:type>/gene/<string:gene>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
@ns.param('type', 'tsne, umap, or pca.')
@ns.param('gene', 'A gene name present in the expression matrix')
class GeneScatterplot(Resource):
    @ns.response(200, 'png scatterplot image')
    def post(self, user, worksheet, type, gene):
        """A png pf a scatter [;pt"""

        cluster = read_cluster(user, worksheet)
        xys = read_xys(user, worksheet)
        centers = centroids(xys, cluster)

        #colormap = {"0": "#FF12FF", "1": "#775656", "2": "#59ad2d", "3": "#FFFF12", "4": "#FFF11F", "5": "#1FFFF1" }

        color_by_cluster = request.is_json
        if color_by_cluster:
            colors = request.get_json()
            color_map = dict(
                zip(
                    colors["cluster-name"],
                    colors["colors"]
                )
            )
            png = scatter_categorical(xys, centers, color_map, cluster)

        else: # Color the scatter plot with an individual gene.
            gene = read_gene_expression(user, worksheet, gene)
            png = scatter_continuous(xys, centers, gene)

        return send_file(
            png,
            mimetype='image/png'
        )


@ns.route('/<string:user>/worksheet/<string:worksheet>/scatterplot/<string:type>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
@ns.param('type', 'tsne, umap, or pca.')
class GeneScatterplot(Resource):
    @ns.response(200, 'png scatterplot image')
    def post(self, user, worksheet, type, gene):
        """A png pf a scatter colored by the requested json."""

        # Generate the scatter plot on the fly.
        cluster = read_cluster(user, worksheet)
        xys = read_xys(user, worksheet)
        centers = centroids(xys, cluster)

        if not request.isjson:
            raise ValueError("endpoint requires json")

        colors = request.get_json()
        color_map = dict(
            zip(
                colors["cluster-name"],
                colors["colors"]
            )
        )

        return send_file(
            scatter_categorical(xys, centers, color_map, cluster),
            mimetype='image/png'
        )


def generate_worksheet(user, worksheet):
    """Generates a worksheet on the fly."""
    marker_dicts = read_json_gzipd(TEST_MARKERS_DICT_PATH)['markers']
    cluster_solution_name = CLUSTER_SOLUTION_NAME
    genes = find_genes(marker_dicts, cluster_solution_name=cluster_solution_name)
    colors = bubble_table(
        marker_dicts,
        genes.tolist(),
        cluster_solution_name=cluster_solution_name,
        attr_name="z_stat"
    )
    sizes = bubble_table(marker_dicts, genes.tolist(), cluster_solution_name=cluster_solution_name,
                         attr_name="specificity")

    resp = {
        "user": "tester", "worksheet": "test", "dataset_name": "krigstien6K-fastfood",
        "size_by": "percent expressed", "color_by": "z statistic",
        "clusters": dataframe_to_str(pd.read_csv(TEST_CLUSTER_TABLE_PATH, sep="\t")),
        "genes": dataframe_to_str(genes),
        "colors": dataframe_to_str(colors),
        "sizes": dataframe_to_str(sizes)
    }
    return resp


def save_worksheet(user, worksheet, pydict):
    with gzip.GzipFile(TEST_STATE_PATH, 'w') as fout:
        fout.write(
            json.dumps(pydict
       ).encode('utf-8'))


def grab_saved_worksheet(user, worksheet):
    try:
        resp = read_json_gzipd(TEST_STATE_PATH)
    except FileNotFoundError:
        resp = None

    return resp


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
    return img_bytes


def centroids(xys, cluster):
    """Returns a dataframe with cluster as index and x and y centroid columns."""
    both = pd.concat([xys,cluster], axis=1)
    both.columns = ["x", "y", "cluster"]
    cluster_centers = both.groupby("cluster").mean()
    return cluster_centers


def gene_table(marker_dicts, cluster_name, cluster_solution_name=CLUSTER_SOLUTION_NAME):
    """Creates a gene table on the fly for a particulat cluster and clustersolution from marker dictionaries."""
    filtered_markers = [d for d in marker_dicts if cluster_solution_name == d["cluster_solution_name"] and cluster_name == d["cluster_name"]]
    genes = [d["gene_name"] for d in filtered_markers]
    t_statistics = [d["mean_expression"] for d in filtered_markers]
    pcent_expressed = [d["sensitivity"] for d in filtered_markers]

    df = pd.DataFrame([genes, t_statistics, pcent_expressed], index=["gene", "mean expression", "percent expressed"]).transpose()
    return df


def bubble_table(marker_dicts, genes, cluster_solution_name, attr_name):
    """Creates a size or color table for the worksheet endpoint."""
    filtered_markers = [d for d in marker_dicts if cluster_solution_name == d["cluster_solution_name"] and d["gene_name"] in genes]
    bubble_values = [{"gene": d["gene_name"], "cluster": d["cluster_name"], "value": d[attr_name]} for d in filtered_markers]
    bubble_values = pd.DataFrame(bubble_values)
    bubble_values = bubble_values.pivot(
        index="gene",
        columns="cluster",
        values="value"
    )

    return bubble_values


def find_genes(marker_dicts, cluster_solution_name, size="sensitivity", color="z_stat"):
    """
    Hack to pick genes to show on dotplot by multiplying size and color variable.
    :param marker_dicts:
    :param cluster_solution_name:
    :param size:
    :param color:
    :return: series with genes of highest color and score product per cluster
    """
    # Grab important marker values for this clustersolution name
    filtered_markers = [
        {"gene": d["gene_name"], "cluster": d["cluster_name"], "size": d[size], "color": d[color]}
        for d in marker_dicts if cluster_solution_name == d["cluster_solution_name"]
    ]

    marker_df = pd.DataFrame(filtered_markers)

    # Simple sorting metric.
    marker_df["product"] = np.abs(marker_df["size"] * marker_df["color"])

    # Return genes that have the highest product per cluster
    genes = marker_df.iloc[marker_df.groupby("cluster", sort=False)["product"].idxmax().tolist()]["gene"]

    # This sets the order of the genes on the client as arbitrary.
    genes.index = pd.RangeIndex(0, len(genes.index))
    return genes


def read_gene_expression(user, worksheet, gene):
    return pd.read_pickle(TEST_EXPRESSION_PICKLE_PATH)[gene]


def read_cluster(user, worksheet):
    return pd.read_pickle(TEST_CLUSTER_ID_PATH)


def read_xys(user, worksheet):
    xys = pd.read_pickle(TEST_XY_PATH)
    xys.columns = ["x", "y"]
    return xys


def read_json_gzipd(filename):
    with gzip.GzipFile(filename, 'r') as fin:
        json_bytes = fin.read()

    json_str = json_bytes.decode('utf-8')
    data = json.loads(json_str)
    return data


def dataframe_to_str(df):
    buffer = io.StringIO()
    df.to_csv(buffer, sep="\t")
    buffer.seek(0)
    return buffer.getvalue()
