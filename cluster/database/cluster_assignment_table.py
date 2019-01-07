
from cluster.database.table import Table
from cluster.database.cluster_table import cluster
from cluster.database.db import get_db


class Cluster_assignment_table(Table):
    table = 'cluster_assignment'  # table name
    parentless_fields = [         # table fields minus row ID
        'name',
    ]
    fields = parentless_fields + ['cluster_id']
    tsv_header = parentless_fields + ['cluster']
    parent = {  # foreign keys in this table
        'field': 'cluster',
        'table': cluster
    }
    # The 'insert into database' string.
    # This is duplicated in each specialized table class
    # because it is built at class instance creation.
    add_one_string = \
        'INSERT INTO ' + table + ' (' + \
        ','.join(fields) + \
        ')' + \
        'VALUES (' + ('?,' * len(fields))[:-1] + ')'


cluster_assignment = Cluster_assignment_table()

