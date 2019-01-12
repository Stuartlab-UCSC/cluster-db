
# TSV database utilites.
import os, csv, sqlite3
from flask import current_app
from cluster.database.db import get_db, lists_equal, merge_dicts
from cluster.database.error import Bad_tsv_header


def requested(accept):
    return (str(accept) == 'text/tsv')


def from_rows(fields, rows):
    # Convert sqlite rows to TSV lines.
    tsv = '\t'.join(fields)  # the header
    for row in rows:
        lis = list(row.values())
        lStr = []
        for l in lis:
            lStr.append(str(l))
        tsv += '\n' + '\t'.join(lStr)
    return tsv


def add(table, tsv_file, parent_name=None):
    # Note: Rows that are too short don't error out,
    #       but will simply add null values at the end.
    #       Rows that are too long are interpreted as a new row and may error
    #       out if non-nulls are required for this bad row.
    f = os.path.join(current_app.config['UPLOADS'], tsv_file)
    with open(f, 'r') as f:
        f = csv.DictReader(f, delimiter='\t')

        # Bail if the file header is not correct.
        if not lists_equal(f.fieldnames, table.parentless_fields):
            raise Bad_tsv_header( \
                'expected: "' + ' '.join(table.parentless_fields) + \
             '"\n   given: "' + ' '.join(f.fieldnames) + '"')
        # If parent names are required ....
        db = get_db()
        if table.parent_table:
             parent_id = table._get_closest_parent_id(parent_name)
             # Add the parent ID to the end of each row before adding to the DB.
             for row in f:
                 row = dict(row)
                 row[table.parent_table[0] + '_id'] = parent_id
                 table._add_one(row, db)
        else:
            # No parents, so simply add the data to the database.
            for row in f:
                table._add_one(row, db)

        db.commit()


