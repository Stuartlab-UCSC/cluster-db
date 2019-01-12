
from cluster.database.table import Table
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.db import get_db


class Cluster_table(Table):
    def __init__(s):
        s.table = 'cluster'     # table name
        s.parentless_fields = [ # table fields minus row ID
            'name',
        ]
        s.fields = s.parentless_fields + ['clustering_solution_id']
        s.parent_table = [ # ancestor tables of this table
            'clustering_solution',
            'dataset'
        ]
        s.child_table = [ # descendent tables of this table
            'attribute',
            'cluster_assignment',
        ]


cluster = Cluster_table()

