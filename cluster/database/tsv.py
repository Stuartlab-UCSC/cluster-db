
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


def load(table, tsv_file, parent_names=None):

    db = get_db()
    f = os.path.join(current_app.config['UPLOADS'], tsv_file)
    with open(f, 'r') as f:
        f = csv.DictReader(f, delimiter='\t')

        # Bail if the file header is not correct.
        if ((f.fieldnames > table.fields) -
            (f.fieldnames < table.fields)) != 0:
            raise Bad_tsv_header('expected: "' + ' '.join(table.fields) + \
                              '"\n   given: "' + ' '.join(f.fieldnames) + '"')

        # Add each tsv row to the table.
        if parent_names:
            # TODO this only handles one parent ID in the row.
            pass
            #for row in f:
            #    row[parent_tables[0]] = parent_name
                 # TODO this is expecting a dict
            #    table.add_with_parent_check(row, db)
        else:
            for row in f:
                # Zip the keys and values together then add to the table.
                # TODO zip
                table.add_one(data)


    #db.commit()


def requested(accept):
    return accept == 'text/tsv'

