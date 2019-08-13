"""
cli exposed via flask *function-name

wrap create_app with the @command_line_interface decorator

`export FLASK_APP=cluster` is necessary.

`flask --help` to show available functions

to add another cli write a click.command() function and add the function name into CLICK_COMMANDS (at bottom of file)
"""
import datetime
import os
import click
from decorator import decorator
import cluster.cli.scanpyapi as ad_obj
import pandas as pd
import numpy as np

from cluster.user_io import make_worksheet_root, save_worksheet, read_markers_df, read_cluster, write_all_worksheet
from cluster.database.user_models import get_all_worksheet_paths, add_worksheet_entries, User
import cluster.database.filename_constants as keys


from flask import current_app
from flask.cli import with_appcontext

from cluster.database import db
from cluster.database.user_models import add_group
from cluster.database.add_entries import add_entries
from .create.worksheet_state import generate_worksheet_state


def ensure_values(reset_df):
    """
    crazy sheme to ensure there are no wierd values going over into the state
    :param df:
    :return:
    """
    # For now just get rid of -inf values
    min = reset_df[0].iloc[(reset_df[0] != -np.inf).tolist()].min()
    max = reset_df[0].iloc[(reset_df[0] != np.inf).tolist()].max()

    reset_df[0].replace({-np.inf: min}, inplace=True)
    reset_df[0].replace({np.inf: max}, inplace=True)

    reset_df.fillna(0, inplace=True)
    return reset_df


@click.command(help="Add a Group to the User Database.")
@click.argument('group_name')
@with_appcontext
def create_group(group_name):
    add_group(db.session, group_name)


@click.command(help="Add a Group to the User Database.")
@click.argument('email')
@click.argument('worksheet_name')
@click.argument('group_name')
@with_appcontext
def add_worksheet_group(email, worksheet_name, group_name):
    from cluster.database.user_models import CellTypeWorksheet, User, Group
    user = User.get_by_email(email)
    ws = CellTypeWorksheet.get_worksheet(user, worksheet_name)
    group = Group.get_by_name(group_name)
    ws.groups = [group, ]
    db.session.add(ws)
    db.session.commit()


@click.command(help="Add worksheet tsvs to user file system.")
@click.argument('user_email')
@click.argument('worksheet_name')
@click.argument('exp_path')
@click.argument('cluster_path')
@click.argument('markers_path')
@click.argument('xys_path')
@with_appcontext
def load_tsv(
        user_email, worksheet_name, exp_path,
        cluster_path, markers_path, xys_path,
):
    try:
        xys = pd.read_csv(xys_path, sep="\t", index_col=0)
        exp = pd.read_csv(exp_path, sep="\t", index_col=0)
        clustering = pd.read_csv(cluster_path, sep="\t", index_col=0)
        clustering = clustering[clustering.columns[0]]
        markers = pd.read_csv(markers_path, sep="\t")
        write_all_worksheet(user_email, worksheet_name, markers=markers, xys=xys, exp=exp, clustering=clustering)

    except FileNotFoundError as e:
        print(e)

@click.command(help="Make a pickle from a tsv.")
@click.argument('fin')
@click.argument('fout')
@click.option('--format', default="tsv")
@click.option('--index_col', default=None)
def to_pickle(fin, fout, format, index_col):
    df = pd.read_csv(fin, sep="\t", index_col=index_col)
    pd.to_pickle(df, fout)

@click.command(help="Create state after loading files.")
@click.argument('user_email')
@click.argument('worksheet_name')
@click.argument('dataset_name')
@click.option('--color_by', default="avg_logFC")
@click.option('--size_by', default="pct.1")
@with_appcontext
def create_state(
        user_email, worksheet_name, color_by, size_by, dataset_name
):
    try:
        ws_paths = get_all_worksheet_paths(user_email, worksheet_name)

        clustering = read_cluster(ws_paths[keys.CLUSTERING])
        markers = read_markers_df(ws_paths[keys.MARKER_TABLE])
        """
        genes = ["TNNT2", "MYL2", "TOP2A", "CENPF", "NR2F1", "PITX2", "SHOX2", "PECAM1", "NPR3", "CLDN5", "LYVE1",
                 "DCN", "POSTN", "ACTA2", "TAGLN", "CSPG4", "RSPO3", "HAPLN1", "WT1", "MPZ", "PRPH", "IL1B",
                 "TPSAB1", "HBG1"]
         """
        genes = []
        state = generate_worksheet_state(
            user_email,
            worksheet_name,
            dataset_name,
            clustering,
            size_by,
            color_by,
            genes=genes,
            markers_df=markers,
        )

        save_worksheet(
            os.path.join(
                make_worksheet_root(user_email, worksheet_name),
                keys.STATE
            ),
            state
        )

    except FileNotFoundError as e:
        print(e)


@click.command(help="Add a scanpy object to the user file system")
@click.argument('user_email')
@click.argument('worksheet_name')
@click.argument('scanpy_path')
@click.option('--cluster_name', default="louvain")
@click.option('--dataset_name', default="")
@click.option('--celltype_key', default="scorect")
@with_appcontext
def load_scanpy(user_email, worksheet_name, scanpy_path, cluster_name,
                dataset_name, size_by="-log10adjp", color_by="mean", celltype_key=None
):
    print("reading in data...")
    ad = ad_obj.readh5ad(scanpy_path)
    mapping = ad_obj.celltype_mapping(ad, cluster_name, celltype_key)
    use_raw = ad_obj.has_raw(ad)
    xys = ad_obj.get_xys(ad, key="X_umap")
    """
    import anndata
    a = anndata.AnnData(ad.raw.X, var=ad.raw.var_names, obs=ad.raw.obs_names)
    a.var_names = a.var['index']
    a.obs_names = a.obs['index']
    mg = ad_obj.mito_genes(a.var_names)
    mean_mg = a[:,mg].X.toarray().sum(axis=1)
    met_genes = ['ALDOA', 'GAPDH', 'MALAT1', 'LDHA', 'PFKFB4', 'HK2']
    mean_met = a[:, met_genes].X.toarray().sum(axis=1)
    outside_RG = ['HOPX', 'PTPRZ1', 'TNC', 'ITGB5','SDC3', 'HS6ST1', 'IL6ST', 'LIFR', 'VIM', 'PTN']
    outside_RG = [f for f in ad.var_names if f in outside_RG]
    oRG =  a[:, outside_RG].X.toarray().sum(axis=1)
    df = pd.DataFrame({"org": oRG, "metabolic signature": mean_met, "mitochondrial signature": mean_mg}, index=a.obs_names)
    #print(df)
    ab = anndata.AnnData(df)


    a = a.transpose()
    ab = ab.transpose()
    ac = a.concatenate(ab)
    ac = ac.transpose()
    ac.obs['louvain'] = ad.obs['louvain']
    ad = ac
    use_raw = False
    """
    means = ad_obj.centroids(ad, cluster_name, use_raw)

    clustering = ad_obj.get_obs(ad, cluster_name)

    #print(ad.var_names)
    # Need to use all of the genes of NA's will come about in the data.
    n_genes = ad_obj.all_genes_n(ad, use_raw)
    print("executing gene ranking...")
    ad_obj.run_gene_ranking(ad, cluster_name, n_genes, use_raw)

    proportions = ad_obj.proportion_expressed_cluster(ad, clustering, use_raw)
    #print(proportions.head())
    scores = ad_obj.parse_ranked_genes(ad, "scores")
    #print(scores.head())
    pvals_adj = ad_obj.parse_ranked_genes(ad, "pvals_adj")
    #print(pvals_adj.head())
    log2fc = ad_obj.parse_ranked_genes(ad, "logfoldchanges")
    #print(log2fc.head())
    # Parse out a markers table from the metrics of interest.
    proportions = proportions.loc[log2fc.index, log2fc.columns]
    means = means.loc[log2fc.index, log2fc.columns]
    pvals_adj = pvals_adj.loc[log2fc.index, log2fc.columns]
    scores = scores.loc[log2fc.index, log2fc.columns]

    proportions = proportions.stack().reset_index()
    means = means.stack().reset_index()
    scores = scores.stack().reset_index()
    pvals_adj = pvals_adj.stack().reset_index()
    log2fc = log2fc.stack().reset_index()

    if scores.shape != pvals_adj.shape or scores.shape != log2fc.shape or means.shape != scores.shape:
        print(scores.isna().sum().sum(), "scores are na")
        print(means.isna().sum().sum(), "means are na")
        print(log2fc.isna().sum().sum(), "log2f are na")
        raise ValueError("Markers table could not be created, likely because Na values existed for some metrics.")

    markers_df = pd.DataFrame(columns=["gene", "cluster", "logfc", "-log10adjp", "mean", "scores", "pct.exp"])
    markers_df["gene"] = scores['level_0'].values
    markers_df["cluster"] = scores['level_1'].astype(str).values
    markers_df["mean"] = means[0].values
    markers_df["logfc"] = log2fc[0].values
    markers_df["-log10adjp"] = -np.log10(pvals_adj[0].values+0.000000000001)
    markers_df["pct.exp"] = proportions[0].values
    markers_df["scores"] = scores[0].values

    markers_df["1 - adjp**2"] = 1 - pvals_adj[0].values ** 2
    not_positive = markers_df.index[log2fc[0].values <= 0]
    markers_df.loc[not_positive, "1 - adjp**2"] = .1

    # hard coded genes for chen lab
    genes=['Tmem163', 'Rgs4', 'Olfm1', 'Nnat', 'Snhg11', 'Cdh4', 'Alas2', 'Car2',
    'Nhlh2', 'H2afz', 'Ddah1', 'Hmgn2', 'Trp73', 'Reln', 'Ppp2r2c',
    'Gm28050', 'Diablo', 'Actb', 'Bpgm', 'Mkrn1', 'Snca', 'Ndnf', 'Blvrb',
    'Nr2f2', 'Hbb-bt', 'Hbb-bs', 'Hbb-y', 'Rspo3', 'Fabp7', '1500009L16Rik',
    'Hmgb2', 'Smad1', 'Gypa', 'Mt3', 'Calb2', 'H2afx', '2810417H13Rik',
    'Zic1', 'Cacna2d2', 'Gpx1', 'Tmem158', 'Hba-x', 'Hba-a1', 'Lhx1',
    'Lhx1os', 'Top2a', 'Cks2', 'Gap43', 'Cd200', 'Pcp4', 'Fech', 'Emx2',
    'Nanos1']
    genes = []

    exp = ad_obj.get_expression(ad, use_raw)

    write_all_worksheet(user_email, worksheet_name, xys=xys, exp=exp, clustering=clustering, markers=markers_df)

    print("making state...")

    state = generate_worksheet_state(
        user_email,
        worksheet_name,
        dataset_name,
        clustering,
        markers_df,
        size_by,
        color_by,
        genes,
        mapping
    )

    state_path = os.path.join(
        make_worksheet_root(user_email, worksheet_name),
        keys.STATE
    )

    save_worksheet(state_path, state)


@click.command(help="See the keys for observation matrix")
@click.argument('scanpy_path')
def scanpy_obs_keys(scanpy_path):
    ad = ad_obj.readh5ad(scanpy_path)
    print(ad.obs_keys())


@click.command(help="Add a new user to the user database.")
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_user(email, password):
    user_manager = current_app.user_manager
    user = {
        "email": email,
        "password": user_manager.hash_password(password),
        "email_confirmed_at": datetime.datetime.utcnow(),
    }

    entry = [(User, user)]
    add_entries(db.session, entry)


@click.command(help="Print all user emails.")
@with_appcontext
def all_users():
    print("\n".join([u.email for u in User.query.all()]))


@click.command(help="Remove cluster_user.db")
@with_appcontext
def clear_users():
    print("removing", current_app.config["USERDB"])
    os.remove(current_app.config["USERDB"])


@click.command(help="Add a new worksheet.")
@click.argument('email')
@click.argument('worksheet_name')
@click.argument('dataset_name')
@click.argument('cluster_name')
@with_appcontext
def create_worksheet(email, worksheet_name, dataset_name, cluster_name):
    add_worksheet_entries(
        db.session,
        email,
        worksheet_name,
        organ=None,
        species=None,
        dataset_name=dataset_name,
        cluster_name=cluster_name,
    )


CLICK_COMMANDS = (
    create_user, create_worksheet, all_users,
    clear_users, load_scanpy, load_tsv, create_state,
    to_pickle, scanpy_obs_keys, create_group,
    add_worksheet_group
)


@decorator
def command_line_interface(func, click_commands=CLICK_COMMANDS, *args, **kwargs):
    app = func(*args, **kwargs)
    for command in click_commands:
        app.cli.add_command(command)

    return app
