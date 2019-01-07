
from cluster.database.table import Table
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.db import get_db


class Cluster_table(Table):
    table = 'cluster'  # table name
    parentless_fields = [         # table fields minus row ID
        'name',
    ]
    fields = parentless_fields + ['clustering_solution_id']
    tsv_header = parentless_fields + ['clustering_solution']
    parent = {  # foreign keys in this table
        'field': 'clustering_solution',
        'table': clustering_solution
    }
    child_tables = [  # tables with foreign keys pointing to this table
        'attribute',
        'cluster_assignment',
    ]
    # The 'insert into database' string.
    # This is duplicated in each specialized table class
    # because it is built at class instance creation.
    add_one_string = \
        'INSERT INTO ' + table + ' (' + \
        ','.join(fields) + \
        ')' + \
        'VALUES (' + ('?,' * len(fields))[:-1] + ')'


cluster = Cluster_table()

