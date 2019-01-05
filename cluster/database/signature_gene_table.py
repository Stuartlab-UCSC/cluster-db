
from cluster.database.table import Table
from cluster.database.signature_gene_set_table import signature_gene_set


class Signature_gene_table(Table):
    fields = [
        'name',
        'signature_gene_set_id'
    ]
    pass


signature_gene = Signature_gene_table()

