from decorator import decorator
import pandas as pd
import numpy as np
import os
import gzip
import json
from tests.settings import TMPDIR

def tmpplace(name, tmpdir=TMPDIR):
    return os.path.join(tmpdir, name)

@decorator
def set_seed(func, seed=1, *args, **kwargs):
    np.random.seed(seed)
    return func(*args, **kwargs)


@set_seed
def npints(*args, **kwargs):
    return np.random.randint(*args, **kwargs)


@set_seed
def npfloats(*args, **kwargs):
    return np.random.rand(*args, **kwargs)


def gen_xy(n_samples=100):
    return pd.DataFrame(npfloats(n_samples, 2), columns=["x", "y"])


def gen_expression(n_samples=100, n_genes=100):
    return pd.DataFrame(npfloats(n_samples, n_genes))


def gen_cluster(n_samples=100, n_clusters=10):
    return pd.DataFrame(npints(0,n_clusters, n_samples), columns=["test"])


def gen_gene_table(n_clusters=10, n_genes=100, n_genes_per_cluster=10):
    n_entries = n_clusters * n_genes_per_cluster
    gene_names = npints(0, n_genes, n_entries)
    clusters = npints(0, n_clusters, n_entries)
    size, color = npfloats(2, n_entries)
    df = pd.DataFrame([gene_names, clusters, size, color], index=["gene", "cluster", "size", "color"])
    return df.transpose()


func_dict = {
    "xys": gen_xy,
    "expression": gen_expression,
    "gene_table": gen_gene_table,
    "cluster_solution": gen_cluster
}

worksheet = {
    "simple": "json"
}



def write_json_gzip(path, dictionary):
    with gzip.GzipFile(path, 'w') as fout:
        fout.write(
            json.dumps(dictionary
       ).encode('utf-8'))


def write_all(tmp_path, funcs=func_dict, jsons={"state": worksheet}):
    [f().to_pickle(os.path.join(tmp_path, name)) for name, f in funcs.items()]
    filepaths = dict([(name, tmpplace(name)) for name, f in funcs.items()])
    [write_json_gzip(tmpplace(name), dictionary) for name, dictionary in jsons.items()]
    filepaths.update(dict([(name, tmpplace(name)) for name, f in jsons.items()]))
    return filepaths