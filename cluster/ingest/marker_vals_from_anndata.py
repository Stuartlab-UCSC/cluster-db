"""
Input a anndata object and cluster string, output a data frame (run_pipe) or tsv (main) with the following columns

            "gene_name" : gene,
            "cluster_name": cluster_name,
            "sensitivity": sensivity, #(+1 read considered a guess) / n cells IN cluster
            "specificity": specificity, #(+1 read considered a guess) (n reads < 1 out of cluster / n cells OUT of cluster)
            "precision": precision, #n +1 reads in cluster / n +1 reads out of cluster
            "accuracy": accuracy,
            "recall": recall, #n +1 reads in cluster / n 0 reads in cluster.
            "t_pval": tpval,
            "z_pval": zpval,
            "z_stat": zstat,
            "t_stat": tstat, #(t statistic of gene expression in / out of cluster)
            "log2_change_vs_min": fold_change_min, #( min cluster.... mincluster will always be 0.
            "log2_change_vs_next": fold_change_next, #(next is the level of the second highest cluster, there for the 2nd cluster will always be 1.
            "mean_expression": centroids.loc[gene, cluster_name]


The log fold changes use a pseudocount of 2. This controls the log fold change when you have small values. For instance
if the smaller average expression was .01, and the largest was 2, without a pseudocount the fold change would be
large. Adding a pseudocount of 2 means you would be comparing the fold change between 2.01 and 4 instead, which is less
that a single log2 fold change... that is what we want because we don't want to favor small changes in expression.

For the Ztest, a +1 read in a cell is considered a positive indication, the proportion of +1 reads in the cluster
is compared with the proportion of +1 reads out of the cluster with the alternative hypothesis being that the proporiton
in the cluster is larger than outside of the cluster.

The t-statistics are done with the in cluster vs out of cluster.
"""
import argparse
import sys
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind
import scanpy as sc
import pandas as pd
import math
import numpy as np
import json
import gzip
from scipy.stats import hypergeom
from scipy.sparse.csr import csr_matrix

def parse_args():

    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-ia',"--anndata", type=str, help="anndata object from scanpy",
                        required=True
                        )

    parser.add_argument('-ic', "--csv", type=str, help="expression counts .csv if different than clustered.ad",
                        required=False, default=None
                        )

    parser.add_argument('-cs', "--cluster_string", type=str, help="anndata.uns key that has a list of all available clusters",
                        required=False
                        )

    parser.add_argument('-o',"--fout", type=str, help="name of directory to put gzipped json file",
                        required=True
                        )

    opts = parser.parse_args()

    anndata, counts, cluster_string, out_file = opts.anndata, opts.csv, opts.cluster_string, opts.fout

    return anndata, counts, cluster_string, out_file





def get_expression(adata, use_raw):
    if use_raw:
        ad = adata.raw
    else:
        ad = adata

    if isinstance(ad.X, csr_matrix):
        df = pd.DataFrame(ad.X.toarray(), index=ad.obs_names, columns=ad.var_names)
    else:
        df = pd.DataFrame(ad.X, index=ad.obs_names, columns=ad.var_names)

    return df.transpose()


def hypergeo_z(actual, mu, std):
    return (actual - mu) / std


def hypergeo_mu_std(n_smaller_set, n_larger_set, total_number_of_genes=30000):
    [M, n, N] = [total_number_of_genes, n_smaller_set, n_larger_set]
    hg = hypergeom(M, n, N)
    return hg.mean(), hg.std()


def hypergeo(gene_intersection, n_smaller_set, n_larger_set,  total_number_of_genes=30000):
    return hypergeom.sf(gene_intersection, total_number_of_genes, n_smaller_set, n_larger_set)


def log2_fold_change(A, B):
    return math.log(A, 2) - math.log(B, 2)


def write_data(out_file, marker_dicts):
    with gzip.GzipFile(out_file, 'w') as fout:
        fout.write(json.dumps({"markers": marker_dicts}).encode('utf-8'))


def get_counts(ad, counts):
    if isinstance(counts, pd.DataFrame):
        return counts
    return get_expression(ad, use_raw=True)

def filter_genes(centroids):
    """returns genes that have std > 0"""
    return centroids.index[(centroids.std(axis=1) != 0).tolist()]

def find_markers(centroids, cutoff=.5):
    # Find the second largest of each centroid
    second_largest = centroids.apply(lambda x: x.nlargest(2).iloc[1], axis=1)
    # Do log transforms with pseudocount
    second_largest = np.log2(second_largest + 2)
    log_centroids = np.log2(centroids + 2)
    # Find the log2 fold change from next highest.
    sdiff = log_centroids.sub(second_largest, axis=0)
    # Keep only genes that have at least 1 log fold change (fold change of 2) higher than next.
    marker_genes = sdiff.index[(sdiff.max(axis=1) >= cutoff).tolist()]

    return marker_genes


def run_pipe(ad, cluster_solution_name="louvain"):
    X = get_counts(ad, None)
    X = X.transpose()
    X = X.dropna(axis='columns', how='all')
    #X = (X / X.sum()) * 10000
    cluster_solution = ad.obs[cluster_solution_name]
    cluster_solution = cluster_solution.dropna()
    print(X.shape)
    print("centroid calc")
    # Calculate each centroid.
    centroids = pd.DataFrame(index=X.columns, columns=cluster_solution.unique())
    print(centroids.shape)
    for cluster_name in cluster_solution.unique():
        cell_names = cluster_solution.index[(cluster_solution == cluster_name).tolist()]
        centroid = X.loc[cell_names].mean(axis=0)
        #print(centroid)
        centroids[cluster_name] = centroid
    print("done, filtering...")

    marker_genes = filter_genes(centroids)
    #marker_genes = find_markers(centroids, cutoff=0)

    #marker_genes = centroids.index.tolist()
    print("found %d possible marker genes" % len(marker_genes))
    #pd.Series(marker_genes).to_csv("trash.txt",index=False)
    # Subset down to only those marker genes.
    X = X[marker_genes]

    # Now go through all the found marker genes and calculate each metric for each cluster.
    #print(marker_genes)
    """
    
    for gene in marker_genes:
        second_largest = centroids.loc[gene].nlargest(2).tolist()[1] + 2
        minimum = centroids.loc[gene].min() + 2
    """
    dfs = []
    for cluster_name in cluster_solution.unique():
        print("calc for cluster name", cluster_name)
        df = pd.DataFrame(index=X.columns, columns=["tstat", "zstat", "log2fc", "zpval", "tpval", "cluster"])
        df['cluster'] = cluster_name

        cell_names = cluster_solution.index[(cluster_solution == cluster_name).tolist()]
        other_cell_names = cluster_solution.index[(cluster_solution != cluster_name).tolist()]
        pseudocount = .1
        df['log2fc'] = np.log2(X.loc[cell_names].mean()+pseudocount) - np.log2(X.loc[other_cell_names].mean()+pseudocount)

        # set up for proportions z test
        expressed_in_cluster = (X.loc[cell_names] > 0).sum()
        expressed_out_cluster = (X.loc[other_cell_names] > 0).sum()

        out_size = len(other_cell_names)
        cluster_size = len(cell_names)

        ztest_df = pd.DataFrame([expressed_in_cluster, expressed_out_cluster])
        ztest = lambda x: proportions_ztest(
            count=[x[0], x[1]],
            nobs=[cluster_size, out_size],
            alternative='larger'
        )

        zstat_zpval = ztest_df.apply(ztest, axis='index')
        zstat = zstat_zpval.apply(lambda x: x[0])
        zpval = zstat_zpval.apply(lambda x: x[1])

        ttest = lambda x: ttest_ind(x[cell_names], x[other_cell_names])
        tstat_tpval = X.apply(ttest, axis="index")
        tstat = tstat_tpval.apply(lambda x: x[0])
        tpval = tstat_tpval.apply(lambda x: x[1])

        df["tstat"] = tstat
        df['tpval'] = tpval
        df["zstat"] = zstat
        df["zpval"] = zpval
        df['gene'] = df.index.tolist()
        dfs.append(df)

    markers_table = pd.concat(dfs, axis=0)
    return markers_table


def main():

    in_file, counts_file, cluster_string, fout = parse_args()

    ad = sc.read(in_file)

    try:
        counts = pd.read_csv(counts_file, index_col=0).transpose()
    except ValueError:
        counts = None
        pass

    marker_dicts = []

    if cluster_string is None:
        cluster_solution_names = ["louvain"]
    else:
        cluster_solution_names = [cluster_string]

    for cluster_solution_name in cluster_solution_names:
        X = get_counts(ad, counts)
        X = X.transpose()
        X = (X / X.sum()) * 10000
        print(X.shape)
        X = X.dropna(axis='columns', how='any')
        print(X.shape)
        print("XXX")
        #print(X["MUSK"].isna().sum())
        #print("Nas: ", X.isna().sum().sum())
        cluster_solution = ad.obs[cluster_solution_name]
        cluster_solution = cluster_solution.dropna()

        # Calculate each centroid.
        centroids = pd.DataFrame(index=X.columns)
        for cluster_name in cluster_solution.unique():
            cell_names = cluster_solution.index[(cluster_solution == cluster_name).tolist()]
            centroid = X.loc[cell_names].mean(axis=0)
            centroids[cluster_name] = centroid

        marker_genes = find_markers(centroids)
        #marker_genes = centroids.index.tolist()
        print("found %d possible marker genes" % len(marker_genes))
        #pd.Series(marker_genes).to_csv("trash.txt",index=False)
        # Subset down to only those marker genes.
        X = X[marker_genes]

        # Now go through all the found marker genes and calculate each metric for each cluster.
        #print(marker_genes)
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
                #print(marker_dict)
                #pd.DataFrame(marker_dicts).to_csv("trash.csv")

    df = pd.DataFrame(marker_dicts)
    df.to_csv(fout, sep="\t",index=False)
    #write_data(out_file, marker_dicts)


if __name__ == "__main__":
    sys.exit(main())
