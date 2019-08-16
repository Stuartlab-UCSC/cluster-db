"""
Input/output functions for user files.

Handles reading of file formats and path munging to directory where user data is kept

TODO: remove 'abort' calls into the the user api code.
"""
import os
import gzip
import json
import pandas as pd
from flask import current_app, abort
from decorator import decorator
import cluster.database.filename_constants as keys
from cluster.database.filename_constants import fname_keys
from cluster.utils import timeit


@decorator
def add_user_dir(func, *args, **kwargs):
    """Adds the user directory to the first argument ('path') of a function"""
    USER_DIRECTORY = current_app.config["USER_DIRECTORY"]
    if type(args[0]) == str:
        modified_path = os.path.join(USER_DIRECTORY, args[0])
        args = (modified_path,) + args[1:]
    return func(*args, **kwargs)


@add_user_dir
def get_user_dir(worksheet_root):
    return worksheet_root


@add_user_dir
def save_worksheet(path, pydict):
    try:
        with gzip.GzipFile(path, 'w') as fout:
            fout.write(
                json.dumps(pydict
                           ).encode('utf-8'))

    except ValueError:
        return abort(404, "The user has not saved a worksheet by this name.")


@add_user_dir
def read_saved_worksheet(path):
    try:
        resp = read_json_gzipd(path)

        if resp is None:
            return abort(404, "worksheet state was empty")

    except FileNotFoundError:
        return abort(404, "User worksheet not saved")

    return resp


def make_worksheet_root(user_email, worksheet_name):
    return os.path.join(user_email, worksheet_name)


@add_user_dir
def write_df(worksheet_root, df, type_key):
    path = os.path.join(worksheet_root, type_key)
    df.to_pickle(path)


@add_user_dir
def read_gene_expression(path, gene):
    return pd.read_pickle(path).loc[gene]


@add_user_dir
def read_cluster(path):
    clustering = pd.read_pickle(path)
    clustering = clustering.astype(str)
    return clustering


def markers_manip(marker_df):
    """Ensures markers dataframe has some format restrictions."""
    marker_df["cluster"] = marker_df["cluster"].astype(str)
    cols = marker_df.columns.tolist()
    cols.insert(0, cols.pop(cols.index('gene')))
    marker_df = marker_df.reindex(columns=cols)
    return marker_df


@add_user_dir
@timeit(id_string="read markers.pi")
def read_markers_df(path):
    df = pd.read_pickle(path)
    df = markers_manip(df)
    return df


@add_user_dir
def read_xys(path):
    xys = pd.read_pickle(path)
    xys.columns = ["x", "y"]
    return xys


@add_user_dir
def read_json_gzipd(path):
    with gzip.GzipFile(path, 'r') as fin:
        json_bytes = fin.read()

    json_str = json_bytes.decode('utf-8')
    data = json.loads(json_str)
    return data


@add_user_dir
def make_new_worksheet_dir(path):
    """Makes a new worksheet directory at the worksheet root 'path'."""
    try:
        os.mkdir(path)

    except FileNotFoundError as UserDoesntHaveWSDir:
        # Make the directory and then try again
        os.mkdir(os.path.dirname(path))
        make_new_worksheet_dir(path)

    except FileExistsError:
        pass


def write_all_worksheet(user_email, worksheet_name, markers=None, xys=None, exp=None, clustering=None):
    worksheet_root = make_worksheet_root(user_email, worksheet_name)
    write_df(worksheet_root, exp, keys.EXPRESSION)
    write_df(worksheet_root, markers_manip(markers), keys.MARKER_TABLE)
    write_df(worksheet_root, xys, keys.XYS)
    write_df(worksheet_root, clustering, keys.CLUSTERING)


def is_valid_file(tarsfilename):
    for key in fname_keys:
        if key in tarsfilename:
            return True
    return False


def name_transform(filename):
    """Returns a valid filename constant for a filename."""
    for key in fname_keys:
        if key in filename:
            return key
    raise ValueError("The file name could not be transformed into a valid filename constant")
