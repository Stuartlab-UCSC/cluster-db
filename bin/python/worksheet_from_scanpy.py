"""
takes in a scanpy and outputs 4 files to a directory of your choice.

assumes 'louvain' is the cluster
"""

import scanpy as sc
import pandas as pd
filename = "/home/duncan/work/sandbox/users/admin@replace.me/krigstein6k/kriegstein6k_clustered.h5ad"


def expression_dataframe(anndata):
    df = pd.DataFrame(anndata.X, index=anndata.obs_names, columns=anndata.var_names)
    return df


ad = sc.read(filename)
exp = expression_dataframe(ad)

exp = exp.transpose()

clustering = ad.obs["louvain"]

exp.shape

sc.tl.rank_genes_groups(ad, 'louvain', method='t-test', n_genes=ad.n_vars)

ad.uns['rank_genes_groups'].keys()
len(ad.uns['rank_genes_groups']['scores'][0])
scores = pd.DataFrame(ad.uns['rank_genes_groups']['scores'], index=ad.uns['rank_genes_groups']['names'])
pvals_adj = pd.DataFrame(ad.uns['rank_genes_groups']['pvals_adj'], index=ad.uns['rank_genes_groups']['names'])
log2fc = pd.DataFrame(ad.uns['rank_genes_groups']['logfoldchanges'], index=ad.uns['rank_genes_groups']['names'])

len(clustering.unique())
len(ad.uns['rank_genes_groups']['scores'])
ad.uns['rank_genes_groups']['names'].shape
ad.uns['rank_genes_groups']['params']
ad.uns['rank_genes_groups']['pvals'].shape