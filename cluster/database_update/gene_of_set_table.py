
from cluster.database_update.table import Table
from cluster.database_update.gene_set_table import gene_set
from cluster.database.db_old import get_db


class Gene_of_set_table(Table):
    def __init__(s):
        s.table = 'gene_of_set'  # table name
        s.parentless_fields = [     # table fields minus row ID
            'name',
        ]
        s.fields = s.parentless_fields + ['gene_set_id']
        s.parent_table = [ # ancestor tables of this table
            'gene_set',
            'cluster_solution',
            'dataset'
        ]
        s.child_table = None


gene_of_set = Gene_of_set_table()

