"""
Protected user endpoints work accessing cell type worksheets.
"""
from flask import send_file, request, abort, current_app
from cluster.database import db
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
    User,
    UserExpression,
    ExpCluster,
    ClusterGeneTable,
    CellTypeWorksheet,
    add_worksheet_entries
)
from cluster.user_io import (
    read_markers_df,
    read_saved_worksheet,
    read_gene_expression,
    read_cluster,
    read_xys,
    save_worksheet,
    make_new_worksheet_dir,
    make_worksheet_root,
    get_user_dir,
    is_valid_file,
    name_transform
)
import cluster.database.filename_constants as keys
from cluster.utils import timeit
import os
import tarfile

matplotlib.use("Agg")
ns = api.namespace('user')


@ns.route('/worksheet/<string:worksheet>')
@ns.param('worksheet', 'The name of the worksheet.')
class WorksheetUpload(Resource):
    @ns.response(200, 'worksheet uploaded', )
    def post(self, worksheet):
        """Load a .tar.gz cell type worksheet file with a signed in user"""
        if not current_user.is_authenticated:
            return abort(403)

        ws_root = make_worksheet_root(current_user.email, worksheet)
        make_new_worksheet_dir(ws_root)
        path = get_user_dir(ws_root)
        file = request.files['file']

        tarfilename = os.path.join(path, file.filename)
        file.save(tarfilename)

        with tarfile.open(tarfilename) as tar:
            members = [m for m in tar.getmembers() if m.isfile() and is_valid_file(m.name)]
            for member in members:
                fout_path = os.path.join(path, name_transform(member.name))
                print(fout_path, "fout path")
                tfile = tar.extractfile(member)
                with open(fout_path, "wb") as fout:
                    fout.write(tfile.read())

        # Now you need to add the worksheet to the database.
        add_worksheet_entries(
            db.session,
            current_user.email,
            worksheet,
            organ=None,
            species=None,
            dataset_name=None,
            cluster_name=None,
        )


def is_valid_file(tarsfilename):
    for key in fname_keys:
        if key in tarsfilename:
            return True
    return False


def name_transform(tarsfilename):
    for key in fname_keys:
        if key in tarsfilename:
            return key
    raise ValueError("The file name could not be transformed into a valid filename constant")


@ns.route('/worksheets')
class UserWorksheets(Resource):
    @ns.response(200, 'worksheet retrieved', )
    def get(self):
        """Retrieve a list of worksheets available to the user """
        if not current_user.is_authenticated:
            return abort(403)

        all_available = []
        users_ws = [
            "%s/%s" % (current_user.email, wsname)
            for wsname in CellTypeWorksheet.get_user_worksheet_names(current_user)
        ]
        all_available.extend(users_ws)
        # So you've got groups in and now you just need to find all the user's groups and then get all the
        # worksheets in that group. do username/worksheet_name. Once you do that then you need you'll need to let the get's happen if
        # there are group permissions.
        for group in current_user.groups:
            worksheet_keys = [
                "%s/%s" % (User.get_by_id(ws.user_id).email, ws.name)
                for ws in CellTypeWorksheet.get_by_group(group.name)
            ]
            all_available.extend(worksheet_keys)

        # remove duplicates from a user's own worksheet being a member of their group.
        all_available = list(set(all_available))
        print('all available worksheets', all_available)
        return all_available
        #return [wsname for wsname in CellTypeWorksheet.get_user_worksheet_names(current_user)]


def worksheet_in_user_group(user_entry, worksheet_entry):
    # Users always belong to their own worksheet.
    if user_entry.id == worksheet_entry.user_id:
        return True
    return bool(len(set(user_entry.groups).intersection(set(worksheet_entry.groups))))

@ns.route('/<string:user>/worksheet/<string:worksheet>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
class Worksheet(Resource):
    @timeit(id_string="get worksheet")
    @ns.response(200, 'worksheet retrieved', )
    def get(self, user, worksheet):
        """Retrieve a saved worksheet."""
        user_email = user
        worksheet_name = worksheet
        if not current_user.is_authenticated:
            return abort(403)

        owns_data = current_user.email == user_email
        requested_worksheet_user = User.get_by_email(user_email)
        print('request from %s accessing %s/%s' % (current_user.email, user_email, worksheet_name))

        worksheet = CellTypeWorksheet.get_worksheet(requested_worksheet_user, worksheet_name)
        belongs_to_group = worksheet_in_user_group(current_user, worksheet)
        if owns_data or belongs_to_group:
            return read_saved_worksheet(worksheet.place)

        return abort(401, "User emails did not match, currently users may only access their own data.")

    @ns.response(200, 'worksheet received')
    def post(self, user, worksheet):
        """Create or update a worksheets state."""
        user_email = user
        worksheet_name = worksheet
        if not current_user.is_authenticated:
            return abort(403)

        state = request.get_json()

        if state is None:
            abort(400, "A json state representation is required in the body of request.")

        owns_space = current_user.email == user_email

        if owns_space:
            user_entry = User.get_by_email(user_email)

            # Write over the state if the worksheet is already present
            try:
                from sqlalchemy.orm.exc import NoResultFound
                ws_entry = CellTypeWorksheet.get_worksheet(user_entry, worksheet_name)
                save_worksheet(ws_entry.place, state)

            # Otherwise, make a new worksheet and save the state.
            except NoResultFound as e:
                from cluster.database.user_models import add_worksheet_entries
                orig_worksheet_email = state['source_user']
                orig_worksheet_user = User.get_by_email(orig_worksheet_email)
                orig_worksheet_name = state['source_worksheet_name']
                #print("**************************************", orig_worksheet_user,  orig_worksheet_name)
                #print("all user ws", [f.name for f in CellTypeWorksheet.get_user_worksheets(orig_worksheet_user)])
                orig_ws_entry = CellTypeWorksheet.get_worksheet(orig_worksheet_user, orig_worksheet_name)

                # Must check that the current user has group access
                if not worksheet_in_user_group(current_user, orig_ws_entry):
                    abort(403)

                paths = get_all_worksheet_paths(orig_worksheet_email, orig_worksheet_name)
                if paths is None:
                    abort(400, "source worksheet could not be determined")

                new_ws_entry = add_worksheet_entries(db.session, current_user.email, worksheet_name, paths_dict=paths)

                state['source_user'] = current_user.email
                state['source_worksheet_name'] = worksheet_name

                make_new_worksheet_dir(
                    make_worksheet_root(current_user.email, worksheet_name)
                )

                 #= CellTypeWorksheet.get_worksheet(current_user, worksheet_name)

                save_worksheet(
                    new_ws_entry.place,  # The worksheet just put in there.
                    state
                )

                print("saved worksheet to %s" % new_ws_entry.place)


@ns.route('/<string:user>/worksheet/<string:worksheet>/cluster/<string:cluster_name>')
@ns.param('user', 'user id')
@ns.param('worksheet', 'The name of the worksheet.')
@ns.param('cluster_name', 'The name of the cluster')
class GeneTable(Resource):
    # @api.marshal_with(all_markers_model, envelope="resource")
    @timeit(id_string="get Gene table")
    @ns.response(200, 'tab delimited genes per cluster file', )
    def get(self, user, worksheet, cluster_name):

        # Hidden pagination api
        # looks for option parameters in the url and
        # if not there or malformed returns entire gene table.
        # TODO: remove or document.
        sort_by = None
        try:

            from werkzeug.exceptions import HTTPException
            sort_by = request.args['sort_by']
            page = int(request.args['page'])
            page_size = 100
            # Throws 400 BAD Request if the arguments aren't there
        except HTTPException as e:
            print(e)
            pass

        """Grab gene metrics for a specified cluster."""
        if not current_user.is_authenticated:
            return abort(403)
        import time
        print("*********************************cluster table params", user, worksheet)
        user_entry = User.get_by_email(user)
        ws_entry = CellTypeWorksheet.get_worksheet(user_entry, worksheet_name=worksheet)
        exp_entry = UserExpression.get_by_worksheet(ws_entry)
        cluster_entry = ExpCluster.get_cluster(exp_entry)
        path = ClusterGeneTable.get_table(cluster_entry).place

        # Make the table and then throw it in a byte buffer to pass over.
        gene_table = read_markers_df(path)
        ts = time.time()
        msk = (gene_table["cluster"] == cluster_name).tolist()

        gene_table = gene_table.iloc[msk]
        cluster_not_there = gene_table.shape[0] == 0
        if cluster_not_there:
            abort(422, "The cluster requested has no values in the gene table")

        gene_table = gene_table.drop("cluster", axis=1)
        te = time.time()
        print('%s  %2.2f ms' % ("before buffer", (te - ts) * 1000))
        buffer = io.StringIO()

        if sort_by is not None:
            gene_table.sort_values(sort_by, ascending=False, inplace=True)
            beginning = page * page_size
            end = (page * page_size) + page_size
            gene_table = gene_table.loc[gene_table.index[beginning:end]]

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
        ws_entry = CellTypeWorksheet.get_worksheet(user_entry, worksheet_name=worksheet)
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


def parse_genes(genes):
    return genes.strip().split(",")


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
        genes = parse_genes(genes)
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
    @timeit(id_string="gene value scatter plot")
    @ns.response(200, 'png scatterplot image')
    def get(self, user, worksheet, type, gene):
        """A png of a scatter plot colored by a genes value"""
        if not current_user.is_authenticated:
            return abort(403)

        from cluster.database.user_models import ExpDimReduct
        # Make the table and then throw it in a byte buffer to pass over.
        user_entry = User.get_by_email(user)
        ws_entry = CellTypeWorksheet.get_worksheet(user_entry, worksheet_name=worksheet)
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
    @timeit(id_string="Cluster scatterplot")
    @ns.response(200, 'png scatterplot image')
    def post(self, user, worksheet, type):
        """A png scatterplot with clusters colored by json color map."""
        if not current_user.is_authenticated:
            return abort(403)

        from cluster.database.user_models import ExpDimReduct
        # Make the table and then throw it in a byte buffer to pass over.
        from cluster.database.user_models import get_all_worksheet_paths
        paths_dict = get_all_worksheet_paths(user, worksheet)
        import cluster.database.filename_constants as keys

        cluster = read_cluster(paths_dict[keys.CLUSTERING])

        xys = read_xys(paths_dict[keys.XYS])

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


def graph_protions(centers, data, color_map):
    """Iterator provides portions of the categorical scatter plot"""
    for label in centers.index:
        xs = data.loc[data['cluster'] == label, 'x']
        ys = data.loc[data['cluster'] == label, 'y']
        cx, cy = (centers.loc[label]["x"], centers.loc[label]["y"])
        color = color_map[label]
        yield xs, ys, cx, cy, color, label


def join_xys_clusters(xys, clustering):
    data = pd.concat([xys, clustering], axis=1)
    data.columns = ["x", "y", "cluster"]
    return data


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
    data = join_xys_clusters(xys, clusters)
    for xs, ys, cx, cy, color, label in graph_protions(centers, data, color_map):
        plt.scatter(
            x=xs,
            y=ys,
            color=color,
            marker=".",
            alpha=1,
        )

        plt.annotate(
            label,
            (cx, cy),
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
    # This is a binning hack to deal with the distributions of count type data.
    # linear color mappings do not do well because of outliers that stretch the scale.
    gene_vector_has_zeros = (gene==0).sum() != 0 and gene.min() == 0
    if gene_vector_has_zeros:
        # Do the binning:
        # one bin for zeros
        # 3 bins for non zeros
        zero_cells = gene.index[gene==0]
        non_zero_cells = gene.index[gene != 0]
        import numpy as np

        first_third = np.percentile(gene[non_zero_cells], 33)
        second_third = np.percentile(gene[non_zero_cells], 66)
        first_third_cells = gene.index[np.logical_and(gene > 0, gene <= first_third)]
        second_third_cells = gene.index[np.logical_and(gene > first_third, gene <= second_third)]
        last_third_cells = gene.index[gene > second_third]

        import matplotlib.colors as colors
        import matplotlib.cm as cmx
        # Set the color map to match the number of species
        n_bins = 4
        z = range(1, n_bins)
        hot = plt.get_cmap('Reds')
        cNorm = colors.Normalize(vmin=0, vmax=n_bins)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=hot)
        label = [
            "0", "0 - %.2g" % first_third, "%.2g - %.2g" % (first_third, second_third),
            "%.2g - %.2g" % (second_third, gene.max())
        ]

        # Plot each of the bins
        for i, cells in enumerate([zero_cells, first_third_cells, second_third_cells, last_third_cells]):
            #plt.scatter(xys.loc[cells, "x"], xys.loc[cells,"y"], marker=".", color=color[i], label=label[i])
            plt.scatter(xys.loc[cells, "x"], xys.loc[cells, "y"], marker=".", color=scalarMap.to_rgba(i), label=label[i])
        plt.legend()

    else:
        sc = plt.scatter(x=xys['x'], y=xys['y'], marker=".", c=gene, alpha=1, cmap=cm, norm=None, edgecolor='none')
        plt.colorbar(sc)

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
    if genes is None:
        return None

    msk = marker_df["gene"].isin(genes).tolist()
    bubble_values = marker_df.iloc[msk][["gene", "cluster", attr_name]]
    bubble_values = bubble_values.pivot(
        index="gene",
        columns="cluster",
        values=attr_name
    )

    return bubble_values
