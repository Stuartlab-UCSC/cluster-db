
from cluster.database_update.table import Table
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database.db import get_db


class Gene_set_table(Table):
    def __init__(s):
        s.table = 'gene_set'  # table name
        s.parentless_fields = [         # table fields minus row ID
            'name',
            'type',
            'method',
        ]
        s.fields = s.parentless_fields + ['cluster_solution_id']
        s.parent_table = [ # ancestor tables of this table
            'cluster_solution',
            'dataset'
        ]
        s.child_table = ['gene_of_set']


gene_set = Gene_set_table()

