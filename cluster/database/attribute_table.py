
from cluster.database.table import Table
from cluster.database.cluster_table import cluster
from cluster.database.db import get_db


class Attribute_table(Table):
    def __init__(s):
        s.table = 'attribute'   # table name
        s.parentless_fields = [ # table fields minus row ID
            'name',
            'value'
        ]
        s.fields = s.parentless_fields + ['cluster_id']
        s.tsv_fields = s.parentless_fields + ['cluster']
        s.parent_table = [ # ancestor tables of this table
            'clustering_solution',
            'dataset'
        ]
        s.cluster_table = cluster


attribute = Attribute_table()

