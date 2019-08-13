"""
Take in a markers.pi and output n-clusters (n markers-*key*.pi) pickle files, one for each cluster in the dataset.

The idea here is to make the markers_table endpoint faster. That will probably mean that instead of creating
*.pi files like we have here, we just serve up the .tsv as a static file. (timing the endpoint resulted in dumping
into a string buffer taking the most time...

The cluster_name to keys mapping for the filenames is kept in a cluster_keys.pi file, that file is a dictionary
that maps cluster names to the *key* of the file names.

The 'cluster' column is removed from the outputted pickles

input is a markers.pi

output arg to a specific directory.
"""
import os
import pickle


def filename_gen(cluster_number):
    return "markers-%d.pi" % cluster_number


def cluster_keys(marker_df):
    """Make the cluster name to key (filename) dict """
    clustering = marker_df["cluster"].unique()
    n_clusters = len(clustering)
    filnames = [filename_gen(cn) for cn in range(n_clusters)]
    key_dict = dict(zip(clustering, filnames))
    return key_dict


def expand_markers(marker_df, key_dict):
    """Make 1 dataframe per cluster. Put in a dict of "keys"-> dataframe"""
    expand_dict = {}
    clustering = marker_df["cluster"].unique()
    for cluster in clustering:
        msk = (marker_df["cluster"] == cluster).tolist()
        subset = marker_df.iloc[msk]
        subset = subset.drop("cluster", axis=1)
        filename = key_dict[cluster]
        expand_dict[filename] = subset

    return expand_dict


def dump_expanded(expand_dict, dirpath):
    for name, df in expand_dict.items():
        fpath = os.path.join(dirpath, name)
        df.to_pickle(fpath)


def dump_dict(dict, dirpath):
    from cluster.database.filename_constants import SPLIT_CLUSTER_DICT
    with open(os.path.join(dirpath, SPLIT_CLUSTER_DICT), 'wb') as fout:
        pickle.dump(dict, fout)

