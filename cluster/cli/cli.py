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
from cluster.database.user_models import get_all_worksheet_paths, add_worksheet_entries, User, Group, Role
import cluster.database.filename_constants as keys


from flask import current_app
from flask.cli import with_appcontext

from cluster.database import db
from cluster.database.user_models import add_role, add_group
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


@click.command(help="Add a User to a Role.")
@click.argument('user_email')
@click.argument('role_name')
@with_appcontext
def add_user_role(user_email, role_name):
    user = User.get_by_email(user_email)
    role = Role.get_by_name(role_name)

    user.roles.append(role)
    db.session.add(user)
    db.session.commit()


@click.command(help="Add a User to a Group.")
@click.argument('user_email')
@click.argument('group_name')
@with_appcontext
def add_user_group(user_email, group_name):
    user = User.get_by_email(user_email)
    group = Group.get_by_name(group_name)

    user.groups.append(group)
    db.session.add(user)
    db.session.commit()

    #add_group(db.session, group_name)


@click.command(help="Add a Role to the User Database.")
@click.argument('role_name')
@with_appcontext
def create_role(role_name):
    add_role(db.session, role_name)


@click.command(help="Add a Group to the User Database.")
@click.argument('group_name')
@with_appcontext
def create_group(group_name):
    add_group(db.session, group_name)


@click.command(help="Add a worksheet to a group in the user database.")
@click.argument('email')
@click.argument('worksheet_name')
@click.argument('group_name')
@with_appcontext
def add_worksheet_group(email, worksheet_name, group_name):
    from cluster.database.user_models import CellTypeWorksheet, User, Group
    user = User.get_by_email(email)
    ws = CellTypeWorksheet.get_worksheet(user, worksheet_name)
    group = Group.get_by_name(group_name)
    ws.groups.append(group)
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
@click.option('--index_col', default=None)
def to_pickle(fin, fout, index_col):
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
                dataset_name, size_by="zstat", color_by="tstat", celltype_key=None
):
    print("reading in data...")
    ad = ad_obj.readh5ad(scanpy_path)
    mapping = ad_obj.celltype_mapping(ad, cluster_name, celltype_key)
    use_raw = ad_obj.has_raw(ad)
    xys = ad_obj.get_xys(ad, key="X_umap")

    from .create.marker_vals_from_anndata import run_pipe
    markers_df = run_pipe(ad, cluster_name)
    clustering = ad_obj.get_obs(ad, cluster_name)

    #print(ad.var_names)
    # Need to use all of the genes of NA's will come about in the data.

    genes = []

    exp = ad_obj.get_expression(ad, use_raw)

    write_all_worksheet(user_email, worksheet_name, xys=xys, exp=exp, clustering=clustering, markers=markers_df)

    print("making state...")

    state = generate_worksheet_state(
        user_email,
        worksheet_name,
        dataset_name,
        clustering,
        size_by,
        color_by,
        genes=genes,
        mapping=mapping,
        markers_df=markers_df
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
    """Create a database entry for a worksheet. Worsheet data should already be in the user's directory"""
    add_worksheet_entries(
        db.session,
        email,
        worksheet_name,
        organ=None,
        species=None,
        dataset_name=dataset_name,
        cluster_name=cluster_name,
    )


@click.command(help="Remove database entries for a worksheet.")
@click.argument('email')
@click.argument('worksheet_name')
@with_appcontext
def remove_worksheet(email, worksheet_name):
    from cluster.database.user_models import delete_worksheet_entries
    delete_worksheet_entries(
        db.session,
        email,
        worksheet_name,
    )
    print("worksheet removed")

CLICK_COMMANDS = (
    create_user, create_worksheet, all_users,
    clear_users, load_scanpy, load_tsv, create_state,
    to_pickle, scanpy_obs_keys, create_role, create_group,
    add_worksheet_group, add_user_role, add_user_group, remove_worksheet
)


@decorator
def command_line_interface(func, click_commands=CLICK_COMMANDS, *args, **kwargs):
    app = func(*args, **kwargs)
    for command in click_commands:
        app.cli.add_command(command)

    return app
