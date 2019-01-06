
from cluster.database.table import Table
from cluster.database.cluster_table import cluster
from cluster.database.db import get_db


class Attribute_table(Table):
    table = 'attribute'  # table name
    parentless_fields = [         # table fields minus row ID
        'name',
        'value'
    ]
    fields = parentless_fields + ['cluster_id']
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


attribute = Attribute_table()

