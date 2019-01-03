
# TSV database utilites.
import os, csv, sqlite3
from flask import current_app
from cluster.database.db import get_db
from cluster.database.error import Bad_tsv_header

def from_rows(rows, fields):
    # Convert sqlite rows to TSV lines.
    tsv = '\t'.join(fields)  # the header
    for row in rows:
        tsv += '\n' + '\t'.join(list(row.values()))
    return tsv

def _lists_equal(l1, l2):
    return ((l1 > l2) - (l1 < l2)) == 0

def add_many(table, tsv_file, parent_names=None):
    # Note: Rows that are too short don't error out,
    #       but will simply add null values at the end.
    #       Rows that are too long are interpreted as a new row and may error
    #       out if non-nulls are required for this bad row.
    f = os.path.join(current_app.config['UPLOADS'], tsv_file)
    with open(f, 'r') as f:
        f = csv.DictReader(f, delimiter='\t')

        # Bail if the file header is not correct.
        #if ((f.fieldnames > table.fields) -
        #    (f.fieldnames < table.fields)) != 0:
        if not _lists_equal(f.fieldnames, table.fields):
            raise Bad_tsv_header('expected: "' + ' '.join(table.fields) + \
                              '"\n   given: "' + ' '.join(f.fieldnames) + '"')

        # If parent_names are required ....
        if table.parent_tables:
            # TODO
            pass

        # Add each tsv row to the table.
        db = get_db()
        for row in f:
            table._add_one(row, db)
        db.commit()


def requested(accept):
    return accept == 'text/tsv'

