
from cluster.database.table import Table


class Dataset_table(Table):

    table = 'dataset'  # table name
    fields = [         # fields without parent table IDs
        'name',
        'species'
    ]
    child_tables = [   # tables with foreign keys to this table
        'clustering_solution'
    ]

    def _add(s, data, db):
        cursor = db.execute('''
            INSERT INTO dataset (
                name,
                species
            )
            VALUES (?,?)
            ''', s._get_vals(data)
        )
        return cursor

    def _delete_children(s, row, db):
        for child in s.child_tables:
            db.execute('DELETE FROM ' + child + \
                ' WHERE ' + s.table + '_id = ?', \
                (row['id'],))
        # TODO: delete children from other tables.


# The table instance.
dataset = Dataset_table()

