import sys
import os

sys.path.append(os.environ.get("CLUSTERDB"))

import argparse
import pandas as pd

def parse_args():

    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-ie',"--e_path", type=str, help="path pickled dataframe",
                        required=True
                        )

    parser.add_argument('-ic', "--cs_path", type=str, help="",
                        required=True
                        )

    parser.add_argument('-im', "--markers_path", type=str, help="",
                        required=True
                        )

    parser.add_argument('-o', "--output", type=str, help="",
                        required=True
                        )

    opts = parser.parse_args()
    e_path, cs_path, markers_path, output = opts.e_path, opts.cs_path, opts.markers_path, opts.output

    return e_path, cs_path, markers_path, output


def proportion_expressed_cluster(exp_df, clustering):
    """
    outputs a dataframe [genes x cluster] that is the percentage that gene is expressed in a cluster
    :param ad: scanpy.Anndata
    :param cluster_solution_name: string, key accessor for ad.obs cluster_solution (
    :return: pandas.DataFrame
    """


    pcent_df = pd.DataFrame(index=exp_df.index)
    for cluster_name in clustering.unique():
        cells_in_cluster = clustering.index[clustering == cluster_name]

        gt0 = (exp_df[cells_in_cluster] > 0).sum(axis=1)
        pcent_df[cluster_name] = gt0 / float(len(cells_in_cluster))

    return pcent_df


def main():
    exp_path, cs_path, markers_path, output = parse_args()
    exp, clustering, markers = pd.read_pickle(exp_path), pd.read_pickle(cs_path), pd.read_pickle(markers_path)

    proportions = proportion_expressed_cluster(exp, clustering)

    proportions = proportions.stack().reset_index()
    proportions.columns = ["gene", "cluster", "proportion"]
    proportions = proportions.sort_values(["gene", "cluster"])
    markers = markers.sort_values(["gene", "cluster"])
    markers["pct.exp"] = proportions["proportion"].values
    pd.to_pickle(markers, output)

    import pandas as pd
    filename = "/home/duncan/work/sandbox/users/admin@replace.me/pbmc_with_pcent_exp/markers.pi"
    df = pd.read_pickle(filename)
if __name__ == "__main__":
    sys.exit(main())
