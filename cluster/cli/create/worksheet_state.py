"""
Creates worksheet state from files needed to view a worksheet.

TODO: when used a second time abstract with a CLI
"""
import json, gzip
from cluster.api.user import dataframe_to_str, bubble_table
import pandas as pd
from scipy.spatial.distance import pdist
from seriate import seriate
# finisising making worksheet from scanpy

def read_genes_csv(filename):
    df = pd.read_csv(filename, index_col=0)
    genes = set()
    for index, row in df.iterrows():
        row.dropna(inplace=True)
        genes = genes.union(set(row.astype(str).tolist()))

    return list(genes)


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
        genes_df = pd.DataFrame(columns=["row", "genes"])
        colors = empty_bubble_table(clustering)
        sizes = empty_bubble_table(clustering)
        clusters = cluster_table(clustering)

    else:
        colors = bubble_table(markers_df, genes, color_by)
        sizes = bubble_table(markers_df, genes, size_by)
        sizes.fillna(0, inplace=True)
        #row_order = seriate(pdist(sizes))
        row_order = range(0, len(genes))
        genes_df = pd.DataFrame({"row": row_order, "genes": genes})
        #col_order = seriate(pdist(sizes.transpose()))
        clusters = cluster_table(clustering, order=None)

        colors.fillna(0, inplace=True)


    jdict = {
        "user": user_email, "worksheet": worksheet_name,
        "dataset_name": dataset_name,
        "size_by": size_by,
        "color_by": color_by,
        "clusters": dataframe_to_str(clusters, index=False),
        "genes": dataframe_to_str(genes_df, index=False),
        "colors": dataframe_to_str(colors),
        "sizes": dataframe_to_str(sizes),
    }
    #print(jdict["colors"])
    return jdict



def empty_bubble_table(clustering):
    colnames = clustering.unique().tolist()

    colnames.insert(0, "gene")
    return pd.DataFrame(columns=colnames)


def cluster_table(clustering, order=None):
    cluster_counts = clustering.value_counts()

    df = pd.DataFrame(
        columns=["column", "cluster",	"cell_count", "bar_color", "cell_type"],
        index=range(len(cluster_counts))
    )

    if order is None:
        df["column"] = df.index
    else:
        df['column'] = order

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
    size_df = marker_df.pivot(
        index="gene",
        columns="cluster",
        values=size
    )

    color_df = marker_df.pivot(
        index="gene",
        columns="cluster",
        values=color
    )
    rank = size_df.std(axis=1) * color_df.std(axis=1)
    #print(rank.head())
    return rank.sort_values()[-40:].index

