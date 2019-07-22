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

@decorator
def add_user_dir(func, *args, **kwargs):
    """Adds the user directory to the first argument ('path') of a function"""
    USER_DIRECTORY = current_app.config["USER_DIRECTORY"]
    if type(args[0]) == str:
        modified_path = os.path.join(USER_DIRECTORY, args[0])
        args = (modified_path,) + args[1:]
    return func(*args, **kwargs)


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


@add_user_dir
def read_gene_expression(path, gene):
    return pd.read_pickle(path).loc[gene]


@add_user_dir
def read_cluster(path):
    clustering = pd.read_pickle(path)
    clustering = clustering.astype(str)
    return clustering


@add_user_dir
def read_markers_df(path):
    return pd.read_pickle(path)


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

