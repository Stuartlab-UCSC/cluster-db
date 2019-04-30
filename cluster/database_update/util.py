
# Utilities for databasee table access.

from cluster.database.db_old import get_db
import cluster.database.error as err
from cluster.database.error import Not_found, Not_found
import cluster.database.tsv as tsv

text_plain = 'text/plain'

def get_by_parent(table, parent_name, return_ids=False):
    # Return rows with the given parent names, without the parent column.
    # Parents is an array of parent names, closest to farthest.
    if return_ids:
        fields = '*'
    else:
        fields = ','.join(table.parentless_fields)
    parent_id = str(table._get_closest_parent_id_by_name(parent_name))
    parent_table = table.parent_table[0]
    query = \
        'SELECT ' + fields + \
        ' FROM ' + table.table + \
        ' WHERE ' + parent_table + '_id' + \
        ' = ' + str(table._get_closest_parent_id_by_name(parent_name))
    cursor = get_db().execute(query)
    rows = cursor.fetchall()
    if len(rows) < 1:
        raise Not_found(table.table + ' with ' + parent_table + \
            ': ' + parent_name[0])
    return rows
