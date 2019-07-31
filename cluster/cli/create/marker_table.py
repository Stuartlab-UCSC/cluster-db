import numpy as np
import scanpy as sc
import math
from statsmodels.stats.proportion import proportions_ztest
from cluster.cli.cli import centroids
from scipy.stats import ttest_ind

"""
import pandas as pd
def kitchen_sink(ad, cluster_name="louvain"):

    X = ad.X.toarray()
    #X = (X / X.sum()) * 10000
    cluster_solution = ad.obs[cluster_name]
    cluster_solution = cluster_solution.dropna()

    # Calculate each centroid.
    centroids = pd.DataFrame(index=X.columns)
    for cluster_name in cluster_solution.unique():
        cell_names = cluster_solution.index[(cluster_solution == cluster_name).tolist()]
        centroid = X.loc[cell_names].mean(axis=0)
        centroids[cluster_name] = centroid

    print("found %d possible marker genes for cluster solution %s in datasest %s" % (len(marker_genes), cluster_solution_name, dataset_name))
    pd.Series(marker_genes).to_csv("trash.txt",index=False)
    # Subset down to only those marker genes.
    X = X[marker_genes]

    # Now go through all the found marker genes and calculate each metric for each cluster.
    print(marker_genes)
    for gene in marker_genes:
        second_largest = centroids.loc[gene].nlargest(2).tolist()[1] + 2
        minimum = centroids.loc[gene].min() + 2

        for cluster_name in cluster_solution.unique():
            gene_centroid = centroids.loc[gene, cluster_name] + 2
            cell_names = cluster_solution.index[(cluster_solution == cluster_name).tolist()]
            other_cell_names = cluster_solution.index[(cluster_solution != cluster_name).tolist()]

            # TP: true positives
            expressed_in_cluster = (X.loc[cell_names, gene] > 0).sum()
            # FN: false negatives
            not_expressed_in_cluster = (X.loc[cell_names, gene] == 0).sum()
            # FP: false positives
            expressed_out_cluster = (X.loc[other_cell_names, gene] > 0).sum()
            # TN: true negatives
            not_expressed_out_cluster = (X.loc[other_cell_names, gene] > 0).sum()
            # FP + TN
            out_size = len(other_cell_names)
            # TP + FN
            cluster_size = len(cell_names)

            # TP / (FP + TP)
            precision = expressed_in_cluster / (expressed_in_cluster + expressed_out_cluster)
            # TP / (FN + TP)
            recall = expressed_in_cluster / (not_expressed_in_cluster + expressed_in_cluster)

            # TP / ( TP + FN)
            sensivity = expressed_in_cluster / cluster_size
            # TN / (FP + TN)
            specificity = not_expressed_out_cluster / out_size

            # Accuracy = (TP+TN)/(TP+TN+FP+FN)
            accuracy = (expressed_in_cluster + not_expressed_out_cluster) / (out_size + cluster_size)

            fold_change_next = log2_fold_change(gene_centroid, second_largest)
            fold_change_min = log2_fold_change(gene_centroid, minimum)

            zstat, zpval = proportions_ztest(
                count=[expressed_in_cluster, expressed_out_cluster],
                nobs=[cluster_size, out_size],
                alternative='larger'
            )

            tstat, tpval = ttest_ind(X.loc[cell_names, gene], X.loc[other_cell_names, gene])

            marker_dict = {
                "gene_name": gene,
                "dataset_name": dataset_name,
                "cluster_solution_name": cluster_solution_name,
                "cluster_name": str(cluster_name),
                "sensitivity": sensivity.item(),  # (+1 read considered a guess) / n cells IN cluster
                "specificity": specificity.item(),
                "precision": precision.item(),  # n +1 reads in cluster / n +1 reads out of cluster
                "accuracy": accuracy.item(),
                "recall": recall.item(),  # n +1 reads in cluster / n 0 reads in cluster.
                "t_pval": tpval.item(),
                "z_pval": zpval.item(),
                "z_stat": zstat.item(),
                "t_stat": tstat.item(),  # (t statistic of gene expression in / out of cluster)
                "log2_change_vs_min": fold_change_min,  # ( min cluster.... mincluster will always be 0.
                "log2_change_vs_next": fold_change_next,
                "mean_expression": centroids.loc[gene, cluster_name].item()
            }

            marker_dicts += [marker_dict]

    raise NotImplementedError


def scanpy_default(ad):
    print(ad.shape)
    # print(ad.obs["louvain"])
    # print(ad.obs["louvain"].astype(str) != "12")
    not_in_12 = ad.obs_names[ad.obs["louvain"].astype(str) != "12"]
    len(not_in_12)
    ad = ad[not_in_12]
    print(ad.shape)
    means = centroids(ad, "louvain")
    from cluster.cli.create.marker_table import log2fc_markers
    # print(log2fc_markers(means))
    # print(len(log2fc_markers(means)), "n makers n log")

    clustering = ad.obs[cluster_name]
    # print(clustering.shape)

    sc.tl.rank_genes_groups(ad, cluster_name, method='t-test', n_genes=ad.n_vars)

    ad.uns['rank_genes_groups'].keys()

    gene_names = ad.var_names
    scores = pd.DataFrame(ad.uns['rank_genes_groups']['scores'], index=gene_names)
    pvals_adj = pd.DataFrame(ad.uns['rank_genes_groups']['pvals_adj'], index=gene_names)
    log2fc = pd.DataFrame(ad.uns['rank_genes_groups']['logfoldchanges'], index=gene_names)

    # Orient the datafra,es the same way so the stacking works
    means = means.loc[gene_names, log2fc.columns]

    means = means.stack().reset_index()

    scores = scores.stack().reset_index()
    pvals_adj = pvals_adj.stack().reset_index()
    log2fc = log2fc.stack().reset_index()

    # For now just get rid of -inf values
    min = log2fc[0].iloc[(log2fc[0] != -np.inf).tolist()].min()
    max = log2fc[0].iloc[(log2fc[0] != np.inf).tolist()].max()

    log2fc[0].replace({-np.inf: min}, inplace=True)
    log2fc[0].replace({np.inf: max}, inplace=True)

    log2fc.fillna(min, inplace=True)

    markers_df = pd.DataFrame(columns=["gene", "cluster", "logfc", "-log10adjp", "mean", "scores"])

    markers_df["gene"] = scores['index'].values
    markers_df["cluster"] = scores['level_1'].astype(str).values

    markers_df["mean"] = means[0].values
    markers_df["logfc"] = log2fc[0].values
    markers_df["-log10adjp"] = -np.log10(pvals_adj[0].values + 0.000000000001)
    markers_df["scores"] = scores[0].values

    return markers_df

def log2fc_markers(centroids):
    # Find the second largest of each centroid
    second_largest = centroids.apply(lambda x: x.nlargest(2).iloc[1], axis=1)
    # Do log transforms with pseudocount
    second_largest = np.log2(second_largest + 2)
    log_centroids = np.log2(centroids + 2)
    # Find the log2 fold change from next highest.
    sdiff = log_centroids.sub(second_largest, axis=0)
    # Keep only genes that have at least 1 log fold change (fold change of 2) higher than next.
    marker_genes = sdiff.index[(sdiff.max(axis=1) >= 1).tolist()]

    return marker_genes


def detail_marker_dicts(marker_genes, centroids, n_xpr, n_not_xpr):
    marker_dicts = []
    for gene in marker_genes:
        second_largest = centroids.loc[gene].nlargest(2).tolist()[1] + 2
        minimum = centroids.loc[gene].min() + 2

        for cluster_name in centroids.columns:
            gene_centroid = centroids.loc[gene, cluster_name] + 2
            expressed_in_cluster = (X.loc[cell_names, gene] > 0).sum()
            # FN: false negatives
            not_expressed_in_cluster = (X.loc[cell_names, gene] == 0).sum()
            # FP: false positives
            expressed_out_cluster = (X.loc[other_cell_names, gene] > 0).sum()
            # TN: true negatives
            not_expressed_out_cluster = (X.loc[other_cell_names, gene] > 0).sum()
            # FP + TN
            out_size = len(other_cell_names)
            # TP + FN
            cluster_size = len(cell_names)

            # TP / (FP + TP)
            precision = expressed_in_cluster / (expressed_in_cluster + expressed_out_cluster)
            # TP / (FN + TP)
            recall = expressed_in_cluster / (not_expressed_in_cluster + expressed_in_cluster)

            # TP / ( TP + FN)
            sensivity = expressed_in_cluster / cluster_size
            # TN / (FP + TN)
            specificity = not_expressed_out_cluster / out_size

            # Accuracy = (TP+TN)/(TP+TN+FP+FN)
            accuracy = (expressed_in_cluster + not_expressed_out_cluster) / (out_size + cluster_size)

            fold_change_next = log2_fold_change(gene_centroid, second_largest)
            fold_change_min = log2_fold_change(gene_centroid, minimum)

            zstat, zpval = proportions_ztest(
                count=[expressed_in_cluster, expressed_out_cluster],
                nobs=[cluster_size, out_size],
                alternative='larger'
            )

            tstat, tpval = ttest_ind(X.loc[cell_names, gene], X.loc[other_cell_names, gene])

        marker_dict = {
                "gene": gene,
                "cluster": str(cluster_name),
                "sensitivity": sensivity.item(),  # (+1 read considered a guess) / n cells IN cluster
                "specificity": specificity.item(),
                "precision": precision.item(),  # n +1 reads in cluster / n +1 reads out of cluster
                "accuracy": accuracy.item(),
                "recall": recall.item(),  # n +1 reads in cluster / n 0 reads in cluster.
                "t_pval": tpval.item(),
                "z_pval": zpval.item(),
                "z_stat": zstat.item(),
                "t_stat": tstat.item(),  # (t statistic of gene expression in / out of cluster)
                "log2_change_vs_min": fold_change_min,  # ( min cluster.... mincluster will always be 0.
                "log2_change_vs_next": fold_change_next,
                "mean_expression": centroids.loc[gene, cluster_name].item()
            }

            marker_dicts += [marker_dict]

    return marker_dicts

def log2_fold_change(A,B):
    return math.log(A, 2) - math.log(B, 2)
"""