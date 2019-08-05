"""
Transform data into a pickle.

TODO: Make CLI when used for second time.
"""
import os
from cluster.database.filename_constants import XYS, CLUSTERING, EXPRESSION

root_dir = "/home/duncan/work/sandbox/users/admin@replace.me/pbmc"



input_fn = "clustering.tsv"
input_path = os.path.join(root_dir, input_fn)

import pandas as pd

df = pd.read_csv(input_path, sep="\t")

input_fout = ".".join(input_path.split(".")[:-1]) + ".pi"

df.to_pickle(input_fout)

df = pd.read_pickle(input_fout)

df[df.columns[0]].value_counts()

cluster_fn = os.path.join(root_dir, CLUSTERING)

filename="/home/duncan/work/trajectory/dockers/seurat-docker/shared/analysis/clustering/graphclust/clusters.csv"
pd.read_csv(filename,index_col=0).to_pickle(cluster_fn)

xys = os.path.join(root_dir, XYS)
filename="/home/duncan/work/trajectory/dockers/seurat-docker/shared/analysis/tsne/2_components/projection.csv"
pd.read_csv(filename, index_col=0).to_pickle(xys)

expfile = os.path.join(root_dir,EXPRESSION)

expression = pd.read_pickle(expfile)
from cluster.database.filename_constants import MARKER_TABLE

mfile = os.path.join(root_dir, MARKER_TABLE)
markers = pd.read_pickle(mfile)
markers.head()

filepath="/home/duncan/work/trajectory/dockers/seurat-docker/shared/analysis/diffexp/graphclust/differential_expression.csv"
n_clusters = 8
df = pd.read_csv(filepath)
genemap = dict(
    zip(
        df["Feature ID"], df["Feature Name"]
    )
)

expression.shape
dexpression = expression.loc[:,expression.columns.isin(df["Feature ID"].unique()).tolist()]
dexpression.shape
np.sum(df["Feature Name"].isna())
mns = pd.Series(dexpression.columns).replace(genemap)
dexpression.columns = mns.values

mexpression = dexpression.loc[:,dexpression.columns.isin(markers['gene'].unique()).tolist()]

mexpression.shape
mexpression.to_pickle(expfile)
mns
df.columns
wexpression = expression[markers['gene'].unique()]