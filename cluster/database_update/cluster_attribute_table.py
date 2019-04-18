
from cluster.database_update.table import Table
from cluster.database_update.cluster_table import cluster
from cluster.database.db_old import get_db


class Attribute_table(Table):
    def __init__(s):
        s.table = 'cluster_attribute'   # table name
        s.parentless_fields = [ # table fields minus row ID
            'name',
            'value'
        ]
        s.fields = s.parentless_fields + ['cluster_id']
        s.tsv_fields = s.parentless_fields + ['cluster']
        s.parent_table = [ # ancestor tables of this table
            'cluster',
            'cluster_solution',
            'dataset'
        ]
        s.cluster_table = cluster


cluster_attribute = Attribute_table()

