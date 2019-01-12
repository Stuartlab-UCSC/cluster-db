
from cluster.database.table import Table
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.db import get_db


class Signature_gene_set_table(Table):
    def __init__(s):
        s.table = 'signature_gene_set'  # table name
        s.parentless_fields = [         # table fields minus row ID
            'name',
            'method',
        ]
        s.fields = s.parentless_fields + ['clustering_solution_id']
        s.parent_table = [ # ancestor tables of this table
            'clustering_solution',
            'dataset'
        ]
        s.child_table = ['signature_gene']


signature_gene_set = Signature_gene_set_table()

