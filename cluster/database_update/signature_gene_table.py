
from cluster.database_update.table import Table
from cluster.database_update.signature_gene_set_table import signature_gene_set
from cluster.database.db import get_db


class Signature_gene_table(Table):
    def __init__(s):
        s.table = 'signature_gene'  # table name
        s.parentless_fields = [     # table fields minus row ID
            'name',
        ]
        s.fields = s.parentless_fields + ['signature_gene_set_id']
        s.parent_table = [ # ancestor tables of this table
            'signature_gene_set',
            'cluster_solution',
            'dataset'
        ]
        s.child_table = None


signature_gene = Signature_gene_table()

