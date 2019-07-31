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
import scanpy as sc
import pandas as pd
import numpy as np

from scipy.sparse.csr import csr_matrix
from cluster.user_io import make_worksheet_root, save_worksheet, read_markers_df, read_cluster, write_all_worksheet
from cluster.database.user_models import get_all_worksheet_paths, add_worksheet_entries, User
import cluster.database.filename_constants as keys

from flask import current_app
from flask.cli import with_appcontext

from cluster.database import db
from cluster.database.add_entries import add_entries
from .create.worksheet_state import generate_worksheet_state


def expression_dataframe(anndata):
    if isinstance(anndata.X, csr_matrix):
        anndata.X = anndata.X.toarray()

    df = pd.DataFrame(anndata.X, index=anndata.obs_names, columns=anndata.var_names)
    return df


def centroids(ad, cs_name="louvain"):
    cluster_solution = ad.obs[cs_name]
    # Calculate each centroid.
    centers = pd.DataFrame(index=ad.var_names)
    for cluster_name in cluster_solution.unique():
        cells_in_cluster = ad.obs.index[ad.obs[cs_name] == cluster_name]
        centroid = pd.Series(
            ad[cells_in_cluster].X.mean(axis=0).tolist()[0],
            index=ad.var_names
        )
        centers[cluster_name] = centroid

    return centers


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
@click.argument('marker1')
@click.argument('marker2')
@click.argument('field')
#@click.option('--format', default="tsv")
#@click.option('--index_col', default=None)
def to_pickle(marker1, marker2, fout, field):
    df = pd.read_csv(marker1, sep="\t", index_col=None)
    df2 = pd.read_csv(marker2, sep="\t", index_col=None)

    df.sort_values(["cluster", "gene"])

    pd.to_pickle(df, fout)
#df["1-adjp*2"]
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
        genes = ["TNNT2", "MYL2", "TOP2A", "CENPF", "NR2F1", "PITX2", "SHOX2", "PECAM1", "NPR3", "CLDN5", "LYVE1",
                 "DCN", "POSTN", "ACTA2", "TAGLN", "CSPG4", "RSPO3", "HAPLN1", "WT1", "MPZ", "PRPH", "IL1B",
                 "TPSAB1", "HBG1"]
        print(genes)
        state = generate_worksheet_state(
            user_email,
            worksheet_name,
            dataset_name,
            clustering,
            markers,
            size_by,
            color_by,
            genes
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
@with_appcontext
def load_scanpy(user_email, worksheet_name, scanpy_path, cluster_name, dataset_name, size_by="-log10adjp", color_by="mean"):
    ad = sc.read(scanpy_path)
    print("read in shape", ad.shape)
    not_in_12 = ad.obs_names[ad.obs["louvain"].astype(str) != "12"]

    ad = ad[not_in_12]
    print(ad.shape)
    means = centroids(ad, cluster_name)
    #from cluster.cli.create.marker_table import log2fc_markers

    clustering = ad.obs[cluster_name]
    #print(clustering.shape)

    sc.tl.rank_genes_groups(ad, cluster_name, method='t-test', n_genes=ad.n_vars)
    print('rank genes done')
    #ad.uns['rank_genes_groups'].keys()

    gene_names = ad.var_names
    scores = pd.DataFrame(ad.uns['rank_genes_groups']['scores'], index=gene_names)
    pvals_adj = pd.DataFrame(ad.uns['rank_genes_groups']['pvals_adj'], index=gene_names)
    log2fc = pd.DataFrame(ad.uns['rank_genes_groups']['logfoldchanges'], index=gene_names)

    # Orient the datafra,es the same way so the stacking is aligned
    means = means[log2fc.columns]
    pvals_adj = pvals_adj[log2fc.columns]
    scores = scores[log2fc.columns]

    means = means.stack().reset_index()

    scores = scores.stack().reset_index()
    pvals_adj = pvals_adj.stack().reset_index()
    log2fc = log2fc.stack().reset_index()

    # For now just get rid of -inf values
    min = log2fc[0].iloc[(log2fc[0] != -np.inf).tolist()].min()
    max = log2fc[0].iloc[(log2fc[0] != np.inf).tolist()].max()

    log2fc[0].replace({-np.inf: min}, inplace=True)
    log2fc[0].replace({np.inf: max}, inplace=True)

    log2fc.fillna(min, inplace=True)

    markers_df = pd.DataFrame(columns=["gene", "cluster", "logfc", "-log10adjp", "mean", "scores"])

    markers_df["gene"] = scores['index'].values
    markers_df["cluster"] = scores['level_1'].astype(str).values

    markers_df["mean"] = means[0].values
    markers_df["logfc"] = log2fc[0].values
    markers_df["-log10adjp"] = -np.log10(pvals_adj[0].values+0.000000000001)

    markers_df["scores"] = scores[0].values

    markers_df["1 - adjp**2"] = 1 - pvals_adj[0].values ** 2

    not_positive = markers_df.index[log2fc[0].values <= 0]
    print(not_positive)
    #markers_df.loc[not_positive, "1 - adjp**2"] = .1
    from cluster.cli.create.worksheet_state import find_genes, read_genes_csv
    #genes=['Pdgfra', 'Lhx5', 'Pvrl3', 'Top2a', 'Ldb2', 'Sox17', 'Slc18a2', 'Col3a1', 'P2ry14', 'Sfrp1', 'Lpl', 'Gdf5', 'Six3']#, 'Spag5', 'Dlx5', 'Ebf1']#, 'Inhba', 'Otx2', 'Ptprz1', 'Cd44']#, 'Neurog2', 'Syt6', 'Grin3a', 'Sox10', 'Pou3f1', '9130024F11Rik', 'Sp9', 'Dnah12']#, 'Lhx1', 'Tle4', 'Gad1']#, 'Naaa', 'Dlx2', 'Unc45b', 'Mfap4', 'Epas1', 'P2ry12', 'Tbx18', 'Ifgbp7', 'Tbr1', 'cdc25c', 'Fezf2', 'Npas1', 'C3ar1', 'Aldh1l1', 'Emr1', 'Sp8', 'Entpd2', 'Btbd17', 'Trem2', 'Kcnj8', 'Satb2', 'Slc6a11', 'Lmo3', 'Gad2', 'Pecam1', 'Tmeme252', 'Folr1', 'Erbb4', 'Slc6a20a', 'Mki67', 'Aqp4', 'Hes5', 'Olig2', 'Fcgr1', 'Sod3', 'Ndnf', 'Gata2', 'Gpr88', 'Tfap2c', 'Foxp2', 'Ebf3', 'Sst', 'Gsx2', 'Bcl11b', 'Kcne2', 'Ushbp1', 'Eomes', 'Htr3a', 'Slc1a3', 'Trp73', 'Vim', 'C1qa', 'Flt4', 'Isl1', 'Abcc9', 'Prokr2', 'Dok5', 'Rxrg', 'Mpeg1', 'Penk', 'Ctss', 'Csf1r', 'Sstr2', 'Nrgn', 'Tiam2', 'Fam107a', 'Pla2g3', 'Dlx1', 'Cdca7', 'Reln', 'Ak7', 'Tshz1', 'Npy', 'Maf', 'Lhx6', 'Ascl1', 'Bcas1', 'Iqca', 'Sgol2', 'nes', 'Pax6']
    #genes = read_genes_csv("/home/duncan/work/sandbox/users/admin@replace.me/chen/20190208_Chen_markers_formats.csv")

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
    #genes = log2fc_markers_vs_mean(means).tolist()
    print(genes)
    #genes = find_genes(markers_df, size_by, color_by)

    xys = pd.DataFrame(ad.obsm["X_tsne"], index=ad.obs_names)
    exp = expression_dataframe(ad).transpose()

    write_all_worksheet(user_email, worksheet_name, xys=xys, exp=exp, clustering=clustering, markers=markers_df)

    print("making state")
    state = generate_worksheet_state(
        user_email,
        worksheet_name,
        dataset_name,
        clustering,
        markers_df,
        size_by,
        color_by,
        genes
    )

    state_path = os.path.join(
        make_worksheet_root(user_email, worksheet_name),
        keys.STATE
    )

    save_worksheet(state_path, state)


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


CLICK_COMMANDS = (create_user, create_worksheet, all_users, clear_users, load_scanpy, load_tsv, create_state, to_pickle)


@decorator
def command_line_interface(func, click_commands=CLICK_COMMANDS, *args, **kwargs):
    app = func(*args, **kwargs)
    for command in click_commands:
        app.cli.add_command(command)

    return app
