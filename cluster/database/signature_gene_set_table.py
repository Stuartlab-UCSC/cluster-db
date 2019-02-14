
from cluster.database.table import Table
from cluster.database.cluster_solution_table import cluster_solution
from cluster.database.db import get_db


class Signature_gene_set_table(Table):
    def __init__(s):
        s.table = 'signature_gene_set'  # table name
        s.parentless_fields = [         # table fields minus row ID
            'name',
            'method',
        ]
        s.fields = s.parentless_fields + ['cluster_solution_id']
        s.parent_table = [ # ancestor tables of this table
            'cluster_solution',
            'dataset'
        ]
        s.child_table = ['signature_gene']


signature_gene_set = Signature_gene_set_table()

