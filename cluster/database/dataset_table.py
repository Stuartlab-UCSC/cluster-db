
from cluster.database.table import Table


class Dataset_table(Table):

    # Define some variables for this specialized table class.
    table = 'dataset'  # table name
    fields = [         # table fields minus parent IDs
        'name',
        'species',
    ]
    child_tables = [   # tables with foreign keys pointing to this table
        'clustering_solution',
    ]

    # This is duplicated in each specialized table class
    # because it is built at class instance creation time.
    add_one_string = \
        'INSERT INTO ' + table + ' (' + \
        ','.join(fields) + \
        ')' + \
        'VALUES (' + ('?,' * len(fields))[:-1] + ')'

    # This is specific to each specialized table class because there may be
    # different or multiple child tables for each specialized table.
    def _delete_children(s, row, db):
        for child in s.child_tables:
            db.execute('DELETE FROM ' + child + \
                ' WHERE ' + s.table + '_id = ?', \
                (row['id'],))
        # TODO: delete children from other tables.


# The table instance.
dataset = Dataset_table()

