
from cluster.database_update.table import Table
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database.db_old import get_db


class Cluster_table(Table):
    def __init__(s):
        s.table = 'cluster'     # table name
        s.parentless_fields = [ # table fields minus row ID
            'name',
            'label',
            'description'
        ]
        s.fields = s.parentless_fields + ['cluster_solution_id']
        s.parent_table = [ # ancestor tables of this table
            'cluster_solution',
            'dataset'
        ]
        s.child_table = [ # descendent tables of this table
            'cluster_attribute',
            'cell_of_cluster',
        ]


cluster = Cluster_table()

