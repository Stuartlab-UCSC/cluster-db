"""
This code data wrangles the 5k-pbmc diffexp.csv files into a markers_table format.
"""
import pandas as pd
filepath="/home/duncan/work/trajectory/dockers/seurat-docker/shared/analysis/diffexp/graphclust/differential_expression.csv"
n_clusters = 8
df = pd.read_csv(filepath)
n_genes = df.shape[0]

markers_table = pd.DataFrame(columns=["gene", "log2fc", "adjp", "mean", "cluster"], index=range(n_genes* n_clusters))

markers_table.loc[0:n_genes, "cluster"] = "1"
markers_table.loc[n_genes:2*n_genes, "cluster"] = "2"
markers_table.loc[2*n_genes:3*n_genes, "cluster"] = "3"
markers_table.loc[3*n_genes:4*n_genes, "cluster"] = "4"
markers_table.loc[4*n_genes:5*n_genes, "cluster"] = "5"
markers_table.loc[5*n_genes:6*n_genes, "cluster"] = "6"
markers_table.loc[6*n_genes:7*n_genes, "cluster"] = "7"
markers_table.loc[7*n_genes:8*n_genes+1, "cluster"] = "8"

markers_table["gene"] = df["Feature Name"].tolist() * 8

markers_table.head()

def mean_key(cluster_name):
    return "Cluster %d Mean Counts" % cluster_name


def log2_key(cluster_name):
    return 'Cluster %d Log2 fold change' % cluster_name


def adjp_key(cluster_name):
    return 'Cluster %d Adjusted p value' % cluster_name


def make_msk(markers_table, cluster_name):
    return (markers_table["cluster"] == str(cluster_name)).tolist()


def get_values(df, key_func, n_clusters):
    values = []
    for i in range(1, n_clusters + 1):
        values.extend(df[key_func(i)].tolist())

    return values

markers_table["mean"] = get_values(df, mean_key, n_clusters=8)
markers_table["adjp"] = get_values(df, adjp_key, n_clusters=8)
markers_table["log2fc"] = get_values(df, log2_key, n_clusters=8)

markers_table.head()

keepers = []
len(markers_table["gene"].unique())
for i, gene in enumerate(markers_table["gene"].unique()):
    if not i % 1000:
        print(gene,i)
    msk = (markers_table["gene"] == gene).tolist()
    if markers_table.iloc[msk]["adjp"].min() < .1:
        keepers.append(gene)

dmarkers_table = markers_table.iloc[markers_table['gene'].isin(keepers).tolist()]
dmarkers_table.shape

from cluster.database.filename_constants import MARKER_TABLE
import os

## YOU WANT TO CHANGE ADJP in the makers to -log10
root_dir = "/home/duncan/work/sandbox/users/test@test.com/pbmc"
markers_path = os.path.join(root_dir, MARKER_TABLE)
dmarkers_table.to_pickle(markers_path)
markers = pd.read_pickle()
len(keepers)

