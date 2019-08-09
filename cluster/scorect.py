#!/usr/bin/env python3

# Lucas Seninge (lseninge)
# Group members: Lucas Seninge
# Last updated: 07-24-2019
# File: scorect_api.py
# Purpose: Automated scoring of cell types in scRNA-seq.
# Author: Lucas Seninge (lseninge@ucsc.edu)
# Credits for help to: Duncan McColl

"""
API automated cell type annotation in scRNA-seq pipeline.

Example usage:

# Load cell to cluster assignments (format: index is cell name and col 1 is clusters)
cluster_assignment = pd.read_csv('cluster_assignment.csv')
# Load reference markers (format: pd dataframe with cell types name as columns)
ref_df = ct.read_markers_from_file('ref_marker.tsv')
# Load gene ranks (format: a pd dataframe with at least columns 'gene' and 'cluster number')
ranked_genes = ct.ranks_from_file('ranks.csv')
# Load background genes into a list of genes
bk_genes = ct.get_background_genes_file('background.txt')
# Scoring
ct_pval, ct_score = ct.celltype_scores(nb_bins=5,
                                        ranked_genes=ranked_genes,
                                        marker_ref=ref_df,
                                        background_genes=bk_genes)
# Assign - return a pandas Series object
ct_assignment = ct.assign_celltypes(cluster_assignment=cluster_assignment,
                                    ct_pval_df=ct_pval,
                                    ct_score_df=ct_score,
                                    cutoff=0.1)
"""


# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from cluster.utils import timeit

# I/O functions
from numpy.core.multiarray import ndarray


def get_background_genes_file(filepath):
    """
    Get background genes from local file for null-hypothesis formulation.
    """
    gene_list = []
    with open(filepath) as file_gene:
        for line in file_gene:
            gene_list.append(line.strip())
    return gene_list


def wrangle_ranks_from_anndata(anndata):
    """
    Wrangle results from the ranked_genes_groups function of Scanpy (Wolf et al., 2018) on louvain clusters.
    """

    # Get number of top ranked genes per groups
    nb_marker = len(anndata.uns['rank_genes_groups']['names'])
    print('Wrangling: Number of markers used in ranked_gene_groups: ', nb_marker)
    print('Wrangling: Groups used for ranking:', anndata.uns['rank_genes_groups']['params']['groupby'])
    # Wrangle results into a table (pandas dataframe)
    top_score = pd.DataFrame(anndata.uns['rank_genes_groups']['scores']).loc[:nb_marker]
    top_adjpval = pd.DataFrame(anndata.uns['rank_genes_groups']['pvals_adj']).loc[:nb_marker]
    top_gene = pd.DataFrame(anndata.uns['rank_genes_groups']['names']).loc[:nb_marker]
    marker_df = pd.DataFrame()
    # Order values
    for i in top_score.columns:
        concat = pd.concat([top_score[[str(i)]], top_adjpval[str(i)], top_gene[[str(i)]]], axis=1, ignore_index=True)
        concat['cluster_number'] = i
        col = list(concat.columns)
        col[0], col[1], col[-2] = 'z_score', 'adj_pvals', 'gene'
        concat.columns = col
        marker_df = marker_df.append(concat)
    return marker_df


def ranks_from_file(filepath, ext=None):
    """
    Read ranked genes per cluster from a file. Uses the read_markers_from_file api.
    See doc for formatting.
    """
    raise NotImplementedError


# Scoring functions
def _get_score_scale(nb_bins, scale='linear'):
    """
    Return a scoring scheme for the bins.
    """
    scores = np.arange(1, nb_bins+1)[::-1]
    scale_dict = {'linear': np.array, 'square': np.square, 'log': np.log}
    return scale_dict[scale](scores)


def _score_one_celltype(nb_bins, ranked_genes, marker_list, background, score_scheme):
    """
    Helper function that scores one cell type for one cluster and take care of the bining.
    Returns a single score.
    """
    # Initialize score
    score = 0
    # Check if its a list of lists
    multiple_rankings_provided = isinstance(ranked_genes, list) and isinstance(ranked_genes[0], list)
    if multiple_rankings_provided:
        n_ranked_genes = 0

        for rank in ranked_genes:
            n_ranked_genes += len(rank)
            size_bin = len(rank) // nb_bins
            for k in range(nb_bins):
                sub_rank = rank[k * size_bin: (k * size_bin) + size_bin]
                score += (score_scheme[k] * len(set(sub_rank).intersection(set(marker_list))))

        N = len(background)
        K = n_ranked_genes
        n = len(set(marker_list).intersection(set(background)))

    else:
        size_bin = len(ranked_genes)//nb_bins
        for k in range(nb_bins):
            sub_rank = ranked_genes[k*size_bin : (k*size_bin)+size_bin]
            score += (score_scheme[k] * len(set(sub_rank).intersection(set(marker_list))))
        # Get pvalue associated with return score
        N = len(background)
        K = len(ranked_genes)
        n = len(set(marker_list).intersection(set(background)))

    pval = _pval_from_null(score=score, N_genes=N, K_top=K, n_markers=n, m_bins=nb_bins)

    return score, pval

@timeit(id_string="score celltypes")
def _score_celltypes(nb_bins, ranked_genes, marker_ref, background, score_scheme):
    """
    Score all celltypes in the reference for one cluster.
    The reference is a dataframe with cell types as columns.
    """
    # Initialize empty score vector
    score_cluster = np.zeros(len(marker_ref))
    pval_cluster = np.zeros(len(marker_ref))
    # Iterate on cell types
    celltypes = marker_ref.keys()
    for i, celltype in enumerate(celltypes):
        # Score each cell type
        score_ct, pval_ct = _score_one_celltype(nb_bins=nb_bins,
                                       ranked_genes=ranked_genes,
                                       marker_list=marker_ref[celltype],
                                       background=background,
                                       score_scheme=score_scheme)
        score_cluster[i] = score_ct
        pval_cluster[i] = pval_ct

    return score_cluster, pval_cluster


def _pval_from_null(score, N_genes, K_top, n_markers, m_bins):
    """
    Get one tail test p-value associated to the input score given null hypothesis.
    For a description of the null-model see documentation.
    """
    # Define probability parameters
    multi_dist = np.array([(N_genes-n_markers)/N_genes]+[(1-((N_genes-n_markers)/N_genes))/m_bins]*m_bins)
    # Get polynomial coefficients of degree K
    coeff = np.polynomial.polynomial.polypow(multi_dist, K_top)
    return np.sum(coeff[score:])


def assign_celltypes(ct_pval_df, ct_score_df, cluster_assignment, cutoff=0.1):
    """
    Assign a cell type to each cell based on its cluster assignment and the scoreCT results.
    """
    # Build dict cluster:cell type according to cutoff. Use score to break ties.
    clust_to_ct = {}
    for cluster, serie in ct_pval_df.iterrows():
        min_pval = serie.min()
        min_idx = np.where(serie.values == min_pval)[0]
        if min_pval > cutoff:
            clust_to_ct[cluster] = 'NA'
        elif len(min_idx) == 1:
            clust_to_ct[cluster] = serie.index[min_idx[0]]
        else:
            # Subset the score_df
            clust_to_ct[cluster] = ct_score_df.iloc[cluster][min_idx].idxmax()
    # get a new pandas series with cell as indexes and cell type as value
    ct_assignments = cluster_assignment.map(clust_to_ct)
    return ct_assignments


def celltype_scores(nb_bins, ranked_genes, marker_ref, background_genes, scale='linear'):
    """
    Score every cluster in the ranking.
    """
    # Initialize score scheme
    score_scheme = _get_score_scale(nb_bins=nb_bins, scale=scale)
    # Initialize empty array for dataframe
    cluster_unique = np.unique(ranked_genes['cluster_number'].values)
    score_array = np.zeros((len(cluster_unique), len(list(marker_ref))))
    pval_array = np.zeros((len(cluster_unique), len(list(marker_ref))))
    for cluster_i in cluster_unique:
        mask = ranked_genes['cluster_number'] == cluster_i
        valid_cluster = ranked_genes[mask]
        cluster_scores, cluster_pval = _score_celltypes(nb_bins=nb_bins,
                                          ranked_genes=valid_cluster['gene'],
                                          marker_ref=marker_ref, background=background_genes,
                                          score_scheme=score_scheme)

        score_array[cluster_i, : ] = cluster_scores
        pval_array[cluster_i, : ] = cluster_pval
    # Array to df
    score_df = pd.DataFrame(index=cluster_unique, data=score_array, columns=list(marker_ref))
    pval_df = pd.DataFrame(index=cluster_unique, data=pval_array, columns=list(marker_ref))
    return pval_df, score_df


# Util functions : plotting, ...
def plot_pvalue(pval_df, clusters, cutoff=0.1):
    """
    Dot plot of pvalue for each cell type in passed clusters.
    """
    # If only one cluster is input as int, convert to list
    if type(clusters) == int:
        clusters = list(clusters)
    # Iterate
    for cluster in clusters:
        sub_serie = pval_df.iloc[cluster].sort_values(ascending=True)
        # Only plot cell types below cutoff
        sub_serie = sub_serie[sub_serie.values < cutoff]
        sns.scatterplot(sub_serie.index, sub_serie.values, marker='+', color='red', s=150)
        plt.ylabel('P-value')
        plt.xticks(rotation=60)
        plt.title('P-value plot for cluster ' + str(cluster))
        plt.show()


def reassign_celltype(cluster_n, cell_type):
    """
    Function for the user to reassign a cell type. This decision can be motivated from investigating the pvalue plot
    and/or the marker list for a certain cluster.
    """
    raise NotImplementedError




