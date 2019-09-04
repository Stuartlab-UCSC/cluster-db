"""
Creates worksheet state from files needed to view a worksheet.

TODO: when used a second time abstract with a CLI
"""
import json, gzip
from cluster.api.user import dataframe_to_str, bubble_table
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
#from seriate import seriate
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
        size_by,
        color_by,
        markers_df=None,
        genes=[],
        mapping=None
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
        clusters = cluster_table(clustering, mapping=mapping)

    else:
        colors = bubble_table(markers_df, genes, color_by)
        sizes = bubble_table(markers_df, genes, size_by)
        sizes.fillna(0, inplace=True)
        #row_order = seriate(pdist(sizes))
        row_order = range(0, len(genes))
        genes_df = pd.DataFrame({"row": row_order, "genes": genes})
        #col_order = seriate(pdist(sizes.transpose()))
        clusters = cluster_table(clustering, order=None, mapping=mapping)

        colors.fillna(0, inplace=True)

    jdict = {
        "source_user": user_email, "source_worksheet_name": worksheet_name,
        "dataset_name": dataset_name,
        "size_by": size_by,
        "color_by": color_by,
        "clusters": dataframe_to_str(clusters, index=False),
        "genes": dataframe_to_str(genes_df, index=False),
        "colors": dataframe_to_str(colors),
        "sizes": dataframe_to_str(sizes),
    }

    return jdict



def empty_bubble_table(clustering):
    colnames = clustering.unique().tolist()

    colnames.insert(0, "gene")
    return pd.DataFrame(columns=colnames)


def cluster_table(clustering, order=None, mapping=None):
    """

    :param clustering:
    :param order:
    :param mapping: pandas series with indecies as cluster names.
    :return:
    """
    cluster_counts = clustering.value_counts()

    df = pd.DataFrame(
        columns=["column", "cluster",	"cell_count", "bar_color", "cell_type"],
        index=range(len(cluster_counts))
    )
    if mapping is not None:
        mapping = mapping.sort_values()
        df["column"] = range(len(cluster_counts))
        df["cell_type"] = mapping.values
        celltype_col = df[["column", "cell_type"]]

        celltype_col = celltype_col.groupby("cell_type").first()['column']
        print(celltype_col)
        for ct in mapping.unique():
            indxs = df.index[df["cell_type"] == ct]
            df.loc[indxs, "bar_color"] = celltype_col.loc[ct]


        #print(mapping)
        mapping[mapping.duplicated()] = ""
        df["column"] = range(len(cluster_counts))
        df["cell_type"] = mapping.values
        df["cluster"] = mapping.index.tolist()


        #df["bar_color"] = range(len(cluster_counts))
        df["cell_count"] = cluster_counts.values

    else:
        df["cluster"] = cluster_counts.index
        df["cell_count"] = cluster_counts.values
        df["bar_color"] = df['column']

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


