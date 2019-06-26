#!/usr/bin/env python3

# Starting with an existing cluster assignments tsv file,
# find the unique cluster names.

import sys
import pandas as pd

input_file = 'clustAssign.tsv'
output_file = 'cluster.tsv'


def main():
    print('processing:', input_file)
    df = pd.read_table(input_file, index_col=0)
    cluster_names = pd.Series(df[df.columns[0]].unique())
    cluster_names.to_csv(output_file, sep="\t", header=True, index=False)


if __name__ == "__main__":
    sys.exit(main())

