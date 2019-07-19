"""
Creates worksheet state from files needed to view a worksheet.

TODO: when used a second time abstract with a CLI
"""

import pandas as pd

from cluster.api.user import gene_table, dataframe_to_str
import os
from cluster.database.filename_constants import MARKER_TABLE, EXPRESSION, CLUSTERING, STATE
import pandas as pd

USER_DIRECTORY="/home/duncan/work/sandbox/users"
ws_name="pbmc"
user="admin@replace.me"
clustering = pd.read_pickle(os.path.join(USER_DIRECTORY, user, ws_name, CLUSTERING))
#clustering = clustering[clustering.columns[0]]
#clustering.to_pickle(os.path.join(USER_DIRECTORY, user, ws_name, CLUSTERING))
markers_df = pd.read_pickle(os.path.join(USER_DIRECTORY, user, ws_name, MARKER_TABLE))
#import numpy as np
#markers_df["-log10_pval"] = -1.0*np.log10(markers_df["adjp"].values)
#markers_df.to_pickle(os.path.join(USER_DIRECTORY, user, ws_name, MARKER_TABLE))
#markers_df.head()
size_by = "-log10_pval"
color_by= "log2fc"

state = generate_worksheet_state(
    user, ws_name, "pbmc", clustering, None, size_by, color_by
)

state_file = os.path.join(USER_DIRECTORY, user, ws_name, STATE)

write_gzip_state(state_file, state)

import json, gzip
def write_gzip_state(out_file, marker_dicts):
    with gzip.GzipFile(out_file, 'w') as fout:
        fout.write(json.dumps(marker_dicts).encode('utf-8'))

def generate_worksheet_state(
        user_email,
        worksheet_name,
        dataset_name,
        clustering,
        markers_df,
        size_by,
        color_by,
        genes=[]
):
    """

    :param user_email:
    :param worksheet_name:
    :param dataset_name:
    :param markers_df:
    :param size_by:
    :param color_by:
    :param clustering:
    :return:
    """

    no_genes = len(genes) == 0
    if no_genes:
        genes = pd.DataFrame(columns=["row", "genes"])

    clusters = cluster_table(clustering)

    colors = bubble_table(None, None, None) or empty_bubble_table(clustering)

    sizes = bubble_table(None, None, None) or empty_bubble_table(clustering)


    jdict = {
        "user": user_email, "worksheet": worksheet_name,
        "dataset_name": dataset_name,
        "size_by": size_by,
        "color_by": color_by,
        "clusters": dataframe_to_str(clusters, index=False),
        "genes": dataframe_to_str(genes, index=False),
        "colors": dataframe_to_str(colors),
        "sizes": dataframe_to_str(sizes),
    }
    return jdict


def bubble_table(marker_df, genes, attr_name):
    """Creates a size or color table for the worksheet endpoint."""
    if genes is None or marker_df is None:
        return None

    bubble_values= marker_df.loc[genes][["cluster", attr_name]]
    bubble_values = bubble_values.pivot(
        index="gene",
        columns="cluster",
        values="value"
    )

    return bubble_values


def empty_bubble_table(clustering):
    colnames = clustering.unique().tolist()

    colnames.insert(0, "gene")
    return pd.DataFrame(columns=colnames)


def cluster_table(clustering):
    cluster_counts = clustering.value_counts()

    df = pd.DataFrame(
        columns=["column", "cluster",	"cell_count", "bar_color", "cell_type"],
        index=range(len(cluster_counts))
    )

    df["column"] = df.index
    df["cluster"] = cluster_counts.index
    df["cell_count"] = cluster_counts.values
    df["bar_color"] = 0
    return df


def find_genes(marker_df, size="pct.1", color="avg_diff"):
    """
    Hack to pick genes to show on dotplot by multiplying size and color variable.
    :param marker_dicts:
    :param cluster_solution_name:
    :param size:
    :param color:
    :return: series with genes of highest color and score product per cluster
    """
    return []

