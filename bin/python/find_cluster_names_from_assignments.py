#!/usr/bin/env python3

# Starting with an existing cluster assignments tsv file,
# find the unique cluster names.

import sys, argparse, csv, traceback

input_file = 'clustAssign.tsv'
output_file = 'clustNames.tsv'

def main():
    print('processing:', input_file)

    with open(input_file, 'r') as fin:
        fin = csv.reader(fin, delimiter='\t')
        unique = []
        next(fin) # skip the header
        for row in fin:
            if row[1] not in unique:
                unique.append(row[1])

    with open(output_file, 'w') as fout:
        fout = csv.writer(fout, delimiter='\t')
        fout.writerow(['cluster name'])
        for one in unique:
            fout.writerow(one)

    print('done')
    return 0

if __name__ == "__main__" :
    try:
        return_code = main()
    except:
        traceback.print_exc()
        return_code = 1
    sys.exit(return_code)

